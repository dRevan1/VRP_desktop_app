from VRP_graph import Graph
from data_handler import Data_handler as dh

class App:
    def __init__(self):
        self.data = dh()
        self.graph = Graph()