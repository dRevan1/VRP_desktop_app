from app import App
from main_window import Main_window
from PyQt6.QtWidgets import QApplication

app: App = App()
q_app = QApplication([])
window = Main_window(app)
window.show()
q_app.exec()