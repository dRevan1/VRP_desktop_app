import data

class Graph:
    def __init__(self, data: data.Data):
        self.data = data
        self.D: list[list[int]] = []
        self.routes: list[list[int]] = []
        
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
            used_capacity += self.data.nodes[route[i]].demand
            next_node = route[i + 1]
        
            if i == (len(route) - 2) or (self.data.nodes[next_node].demand + used_capacity) > self.data.capacity:
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