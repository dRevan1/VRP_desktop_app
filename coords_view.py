from PyQt6.QtWidgets import QWidget
from graph_view import Graph_view
from PyQt6.QtGui import QPainter, QPen, QColor, QFont

class Coords_view(QWidget):
    def __init__(self, view: Graph_view):
        super().__init__()
        self.view = view
        self.x = self.y = 0
        self.view.mouse_coords.connect(self.update_coords)
    
    
    #----------------------------------------
    # aktualizuje súradnice zo signálu z view
    #----------------------------------------
    def update_coords(self, x, y):
        self.x, self.y = x, y
        self.update()
    #--------------------------------------------------------------------------------------------
    # vykreslenie aktuálnej súradnice podľa kurzora v grafe, súradnice sa aktualizujú z self.view 
    #--------------------------------------------------------------------------------------------
    def paintEvent(self, a0):       
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor('black'), 1)
        font = QFont("Arial", 12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(1, 20, "[" + str(round(self.x, 2)) + ", " + str(round(self.y * -1, 2)) + "]")
        painter.end()