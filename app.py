from VRP_graph import Graph
from data_handler import Data_handler as dh

class App:
    def __init__(self):
        self.data = dh()
        self.graph = Graph()
        self.graph_changed = False # flag či bola vykonaná nejaká zmena - pridanie/vymazanie vrchola/hrany atd., podľa toho sa pýta užívateľa pri rôznych akciách, či chce uložiť súbor
        self.project_name = "New project"
        
        
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