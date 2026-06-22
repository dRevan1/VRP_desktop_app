from app import App
from main_window import Main_window
from PyQt6.QtWidgets import QApplication

app: App = App()
app.data.load_data("network_test_V1.txt", app.graph)
app.graph.complete_distance_matrix()
q_app = QApplication([])
window = Main_window(app)
window.show()
q_app.exec()
#data.save_data("network_test_V2.txt", True, VRP_graph)