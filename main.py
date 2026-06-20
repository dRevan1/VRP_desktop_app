import VRP_graph as VRP
import data_handler as dh

data = dh.Data_handler()
VRP_graph = VRP.Graph()
data.load_data("network_test_V2.txt", VRP_graph)
#data.save_data("network_test_V2.txt", True, VRP_graph)