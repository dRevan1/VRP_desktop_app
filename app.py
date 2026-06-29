from VRP_graph import Graph, queue
from data_handler import Data_handler as dh
import numpy as np
from node import Node
from edge import Edge
from virtual_edge import Virtual_edge as V_edge

class App:
    def __init__(self):
        self.data = dh()
        self.graph = Graph()
        self.project_name = "New project"
        self.selected_menu_tool = 0 # od 0 postupne, ako sú v okne - 0 = kurzor, 1 = node, 2 = edge
        self.graph_change = False
        self.refreshed = True
        
        
    #--------------------------------------------------------------------------------------------------
    # metóda na načítanie siete zo súbora a vytvorenie matice vzdialeností, volá sa z GUI (main_window)
    #--------------------------------------------------------------------------------------------------
    def load_new_network(self, file_path):
        self.graph.init_structures()
        self.data.load_data(file_path, self.graph)
        self.graph.complete_distance_matrix()
    #----------------------------------------------------------------
    # metóda na uloženie siete do súbora, volá sa z GUI (main_window)
    #----------------------------------------------------------------
    def save_network(self, file_path: str, save_D: bool):
        self.data.save_data(file_path, save_D, self.graph)
    #------------------------------------------------------------------------------
    # nastaví centrum podľa vrchola s daným ID - pre grafické rozhranie v aplikácii
    #------------------------------------------------------------------------------
    def set_center(self, node_ID):
        if node_ID == self.graph.center:
            return
        
        if self.graph.center != 0:
            self.graph.nodes[self.graph.node_ID_map[self.graph.center]].set_default()
        self.graph.nodes[self.graph.node_ID_map[node_ID]].set_center()
        self.graph.center = node_ID
    #----------------------------------------------------------------------
    # pridanie vrchola do grafu - pridaný do zoznamu a do výstupnej hviezdy
    #----------------------------------------------------------------------
    def add_node(self, x: float, y: float):
        name = "Node" + str(self.graph.next_node_ID)
        node = Node(self.graph.next_node_ID, x, -y, 0, name, 0)
        
        self.graph.nodes.append(node)
        self.graph.edges_star.extend([] for node in range(len(self.graph.nodes)))
        for row in self.graph.D:
            row.append(-1)
        row = [-1 for col in range(len(self.graph.nodes))]
        row[-1] = 0
        self.graph.D.append(row)
        
        self.graph.node_ID_map[self.graph.next_node_ID] = len(self.graph.nodes) - 1
        self.graph.next_node_ID += 1
        self.graph.isolated_nodes += 1
        self.graph.connected = False
        
        return node
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # vymaže vrchol, na začitaku sa podľa vyššieho ID uložia ID jeho hrán, aby sa vymazali od najvyššieho ID, teda smerom doľava sa indexovanie podľa ID maapy nepokazí, na konci sa potom
    # raz zavolá upravenie ID a prepočet matice D, ak bol mazaný vrchol posledný izolovaný a nemal hrany, treba prepočítať D a tým skontrolovať prepojenie grafu
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def remove_node(self, node: Node, prior_q: list):
        index = self.graph.node_ID_map[node.ID]
        edge_ID = 0
        edge_index = 0
        star_count = len(self.graph.edges_star[index])
        if node.ID == self.graph.center:
            self.graph.center = 0
        while len(prior_q) > 0:
            _, edge_ID = queue.heappop(prior_q)
            edge_index = self.graph.edge_ID_map[edge_ID]
            self.remove_edge(self.graph.edges[edge_index])
        
        self.graph.node_ID_map.pop(node.ID)
        self.graph.nodes.pop(index)
        self.graph.edges_star.pop(index) 
        self.graph.isolated_nodes -= 1 # ak nemá hrany, bol izolovaný, teda dáme -1, ale rovnako aj keď mal hrany, lebo pri mazaní poslednej sa označí ako izolovaný v "remove_edge"
        self.update_node_IDs(index)
        
        if star_count == 0 and self.graph.isolated_nodes == 0: # ak mal vrchol hrany, na konci sa prepočíta D a zistí spojitosť siete, aktualizujú sa ID hrán
            self.graph.reset_D()
            self.graph.complete_distance_matrix()
        elif star_count > 0: # ak nemal vrchol hrany a bol posledný izolovaný (bez hrán), prepočíta sa D a zistí, či je graf spojený
            self.update_edge_IDs(edge_index)          
    #------------------------------------------------------------------------------------------------------------------------------
    # pokúsi sa nájsť hranu medzi danými vrcholmi - používa sa pri pridávaní hrany, ak sme vybrali 2 vrcholy, kde už hrana existuje
    #------------------------------------------------------------------------------------------------------------------------------
    def find_edge(self, _from, to):
        for out in self.graph.edges_star[self.graph.node_ID_map[_from]]:
            if (out._from == _from and out.to == to): return True
        
        return False
    #----------------------------------------------------------------------------------
    # vráti hrany daného vrchola - list a prioritný front, list pre grafické prostredie
    #----------------------------------------------------------------------------------
    def get_nodes_edges(self, node: Node):
        prior_q = []
        edge_list = []
        for out_edge in self.graph.edges_star[self.graph.node_ID_map[node.ID]]:
            queue.heappush(prior_q, (-out_edge.ID, out_edge.ID))
            edge_list.append(self.graph.edges[self.graph.edge_ID_map[out_edge.ID]])
            
        return edge_list, prior_q   
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # pridá hranu do štruktúr - do zoznamu a do hviezdy (aj symetricky), potom zníži počet izolovaných vrcholov, ak nejaké tvoriace hranu boli, následne sa prepočíta matica D
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def add_edge(self, _from: int, to: int):
        if self.find_edge(_from, to):
            return None
        
        _from_node = self.graph.nodes[self.graph.node_ID_map[_from]]
        to_node = self.graph.nodes[self.graph.node_ID_map[to]]
        from_np = np.array([_from_node.pos().x(), _from_node.pos().y()])
        to_np = np.array([to_node.pos().x(), to_node.pos().y()])
        cost = round(np.linalg.norm(from_np - to_np), 2)
        edge = Edge(self.graph.next_edge_ID, _from, _from_node.pos().x(), _from_node.pos().y(), to, to_node.pos().x(), to_node.pos().y(), cost)
        sym_edge = Edge(self.graph.next_edge_ID, to, to_node.pos().x(), to_node.pos().y(), _from, _from_node.pos().x(), _from_node.pos().y(), cost)
        
        self.graph.edges.append(edge)
        self.graph.edges_star[self.graph.node_ID_map[_from]].append(edge)
        self.graph.edges_star[self.graph.node_ID_map[to]].append(sym_edge)
        
        if len(self.graph.edges_star[self.graph.node_ID_map[_from]]) == 1: self.graph.isolated_nodes -= 1
        if len(self.graph.edges_star[self.graph.node_ID_map[to]]) == 1: self.graph.isolated_nodes -= 1
        self.graph.reset_D()
        self.graph.complete_distance_matrix()
        self.graph.edge_ID_map[self.graph.next_edge_ID] = len(self.graph.edges) - 1
        self.graph.next_edge_ID += 1
        
        return edge
    #-----------------------------------------------------------------------------
    # odstráni hranu - z hviezdy (aj symetrickú, má rovnaké ID) a potom zo zoznamu
    #-----------------------------------------------------------------------------
    def remove_edge(self, edge: Edge):
        index = self.graph.edge_ID_map[edge.ID]
        star_list = self.graph.edges_star[self.graph.node_ID_map[edge._from]]
        self.graph.edge_ID_map.pop(edge.ID)
        
        for i in range(len(star_list)):
            if star_list[i].ID == edge.ID:
                star_list.pop(i)
                break
        star_list = self.graph.edges_star[self.graph.node_ID_map[edge.to]]
        for i in range(len(star_list)):
            if star_list[i].ID == edge.ID:
                star_list.pop(i)
                break
        if len(self.graph.edges_star[self.graph.node_ID_map[edge._from]]) == 0: self.graph.isolated_nodes += 1
        if len(self.graph.edges_star[self.graph.node_ID_map[edge.to]]) == 0: self.graph.isolated_nodes += 1
        
        self.graph.edges.pop(index)
    #-----------------------------------------------------------------------------------------------------------
    # upraví ID po mazaní - od indexu najviac vľavo, kde sa mazala hrana, až po koniec zoznamu sa aktualizujú ID
    # tiež prepočíta maticu D
    #-----------------------------------------------------------------------------------------------------------
    def update_edge_IDs(self, index):
        for i in range(index, len(self.graph.edges)):
            self.graph.edge_ID_map[self.graph.edges[i].ID] = i
            
        self.graph.reset_D()
        self.graph.complete_distance_matrix()
    #--------------------------------------
    # aktualizácia node ID, ako pri edge ID
    #--------------------------------------
    def update_node_IDs(self, index):
        for i in range(index, len(self.graph.nodes)):
            self.graph.node_ID_map[self.graph.nodes[i].ID] = i