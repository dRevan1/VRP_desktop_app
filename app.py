from VRP_graph import Graph
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
    #
    #
    #
    def remove_node(self):
        True
    #------------------------------------------------------------------------------------------------------------------------------
    # pokúsi sa nájsť hranu medzi danými vrcholmi - používa sa pri pridávaní hrany, ak sme vybrali 2 vrcholy, kde už hrana existuje
    #------------------------------------------------------------------------------------------------------------------------------
    def find_edge(self, _from, to):
        for out in self.graph.edges_star[self.graph.node_ID_map[_from]]:
            if (out._from == _from and out.to == to): return True
        
        return False
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
    #
    #
    #
    def remove_edge(self):
        True