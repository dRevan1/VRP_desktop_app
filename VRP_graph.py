from node import Node
from edge import Edge
import heapq as queue
import numpy as np

class Graph:
    def __init__(self):
        self.init_structures()
     
     
    #-----------------------------------------------------------------------------------------------------------------------------
    # inicializuje štruktúry, použije sa tiež napríklad pri načítavaní novej siete v aplikácii alebo keď sa vytvorí nový "projekt"
    #-----------------------------------------------------------------------------------------------------------------------------
    def init_structures(self):
        self.nodes: list[Node] = []  # vrcholy
        self.edges_star: list[list[Edge]] = [] # hrany - hviezda, pre každý vrchol obsahuje list jeho hrán
        self.edges: list[Edge] = [] # zoznam hrán - na zápis
        self.capacity: int = 0 # kapacita vozidiel
        self.center: int = 0
        self.mode_edges: int = 0
        self.D: list[list[int]] = []
        self.routes: list[list[int]] = []
        self.ID_map: dict[int, int] = {}
        self.next_ID = 1
        self.connected = True
        self.isolated_nodes = 0
    #-------------------------------------------------------------------------------
    # skontroluje veci na výpočet - či je inicializovaná matica D a listy s vrcholmi
    #-------------------------------------------------------------------------------
    def complete_distance_matrix(self):
        if len(self.nodes) == 0:
            return 1, "Completing distance matrix failed - nodes list is empty!"
        if len(self.D) == 0:
            return 1, "Completing distance matrix failed - base matrix was not initialized!"
        
        for i in range(len(self.D)):
            isolated = True # ak je vrchol izolovaný, tak sa to označí, aby sa potom vykreslil s označením
            for j in range(len(self.D[i])):
                if self.D[i][j] != -1:
                    if self.D[i][j] != 0:
                        isolated = False
                    continue
                result, distance, *_ = self.run_A_star(i, j) # nájde (možno) cestu medzi vrcholmi i a j a vráti jej cenu, pokiaľ taká nie je z načítaných hrán
                if result == 0: # ak sa našla cesta - cena sa symetricky priradí
                    isolated = False
                    self.D[i][j] = self.D[j][i] = distance
            if isolated:
                self.isolated_nodes += 1
                self.connected = False
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # implementácia algoritmu A*, pokúsi sa nájsť najkratšiu cestu medzi vrcholmi s ID start (začiatok) a end (koniec), ak nájde, vráti výsledok a úspešnosť "0", inak "1"
    # berie index vrcholov ako parametre, teda od 0
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def run_A_star(self, start_node, end_node):
        result, path_cost, path = 1, -1, [] # result = úspešnosť, zmení sa na 0 ak sa cesta nájde
        g = [float('inf') for node in range(len(self.nodes))] # ohodnocovacia funkcia g, na začiatku sú hodnoty "nekonečno", teda najdrahšia hrana + 1
        g[start_node] = 0
        pred = [-1 for node in range(len(self.nodes))] # vektor s predchodcami, na získanie výslednej cesty
        prior_q = [] # toto bude prioritný front
        queue.heappush(prior_q, (0, start_node))
        
        while(len(prior_q) > 0):
            _, _from = queue.heappop(prior_q)
            if _from == end_node:
                result = 0
                break
            for edge in self.edges_star[_from]:
                to = edge.to - 1 # v hranách sú ID, takže pre index treba - 1
                if (g[_from] + edge.cost) < g[to]:
                    pred[to] = _from # nastavenie predchodcu pre koncový vrchol
                    g[to] = g[_from] + edge.cost # nastavenie značky pre koncový vrchol
                    from_np = np.array([self.nodes[to].pos().x(), self.nodes[to].pos().y()])
                    to_np = np.array([self.nodes[end_node].pos().x(), self.nodes[end_node].pos().y()])
                    h = np.linalg.norm(from_np - to_np) # hodnota h - predpokladaná vzdialenosť od daného vrcholu do konca - získaná cez L2 normu
                    priority = g[to] + h # priorita je súčet g a h, teda ohodnocovacích funkcií
                    queue.heappush(prior_q, (priority, to))
        
        if result == 0:
            path_cost = g[end_node]
            node = end_node
            while node != start_node:
                path.append(node)
                node = pred[node]
            
            path.append(start_node)
            path.reverse()
        
        return result, path_cost, path
    #-------------------------------------------------------------------------------------------------------------------------------
    # vráti riešenie TSP pomocou metódy najbližšieho suseda zo zadaného indexu, index v parametre je číslo vrchola, teda začína od 1 
    #-------------------------------------------------------------------------------------------------------------------------------
    def get_route_NN(self, start_node):
        no_nodes = len(self.data.nodes)
        nodes_in_route = [0] * no_nodes  # vektor značiek pre prejdené vrcholy
        route = []
        nodes_in_route[start_node - 1] = 1
        route.append(start_node - 1)
        route_length = 0
    
        for i in range(no_nodes - 1):
            nearest_neighbor = 0
            nearest_length = 5000000
            current_node = route[-1]  # posledný prvok v ceste - hľadáme jeho najbližšieho suseda
        
            for j in range(no_nodes):
                if (self.D[current_node][j] < nearest_length and nodes_in_route[j] == 0):
                    nearest_neighbor = j
                    nearest_length = self.D[current_node][j]
                
            route.append(nearest_neighbor)
            nodes_in_route[nearest_neighbor] = 1
            route_length += self.D[current_node][nearest_neighbor]
    
        route.append(start_node - 1)  # nakoniec sa pridá počiatočný vrchol na uzavretie trasy
    
        return route, route_length 
    #-------------------------------------------------------------------------------------------------------------------------------------------------
    # rozdelí trasu získanú v "get_route_NN" ako výsledok TSP na jednotlivé jazdy/zhluky, ktoré následne vráti aj s využitou kapacitou pre každú jazdu
    #-------------------------------------------------------------------------------------------------------------------------------------------------
    def get_subtoures(self, route):
        self.routes = []
        used_capacity = 0
        subtour = []
        subtour.append(route[0])
    
        for i in range(1, len(route) - 1):
            subtour.append(route[i])
            used_capacity += self.nodes[route[i]].demand
            next_node = route[i + 1]
        
            if i == (len(route) - 2) or (self.nodes[next_node].demand + used_capacity) > self.capacity:
                subtour.append(route[0])
                self.routes.append((subtour, used_capacity))
                subtour = []
                subtour.append(route[0])
                used_capacity = 0
    #------------------------------------------------------------------------------------------------------------------------
    # pomocná metóda, ktorá zoberie subtoures tuple (list vrcholov, využitá kapacita) a spraví z každej jazdy string na print
    #------------------------------------------------------------------------------------------------------------------------
    def get_subtoures_strings(subtoures):
            strings = []
            for i in range(len(subtoures)):
                string = ""
                subtour_tuple = subtoures[i]
            
                for j in range(len(subtour_tuple[0]) - 1):
                    string += f"{subtour_tuple[0][j] + 1}->"
                string += f"{subtour_tuple[0][0] + 1}\nUsed capacity: {subtour_tuple[1]}"
                strings.append(string)
            
            return strings