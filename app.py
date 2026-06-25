from VRP_graph import Graph
from data_handler import Data_handler as dh
from node import Node

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
    #----------------------------------------------------------------------
    # pridanie vrchola do grafu - pridaný do zoznamu a do výstupnej hviezdy
    #----------------------------------------------------------------------
    def add_node(self, x: float, y: float):
        name = "Node" + str(self.graph.next_ID)
        node = Node(self.graph.next_ID, x, -y, 0, name, 0)
        
        self.graph.nodes.append(node)
        self.graph.edges_star.extend([] for node in range(len(self.graph.nodes)))
        for row in self.graph.D:
            row.append(-1)
        row = [-1 for col in range(len(self.graph.nodes))]
        row[-1] = 0
        self.graph.D.append(row)
        
        self.graph.ID_map[self.graph.next_ID] = len(self.graph.nodes) - 1
        self.graph.next_ID += 1
        self.graph.connected = False
        
        return node
    #
    #
    #
    def remove_node(self):
        True
    #
    #
    #
    def remove_node(self):
        True
    #
    #
    #
    def remove_edge(self):
        True