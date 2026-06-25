from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QColor, QBrush

class Node(QGraphicsEllipseItem):
    def __init__(self, ID: int, posX: float, posY: float, demand: int, name: str, type: int):
        super().__init__(-8.0 / 2, -8.0 / 2, 8.0, 8.0)
        self.setPos(posX, -posY)
        self.color = QColor("black") if type == 0 else QColor("green")
        self.setBrush(QBrush(self.color))
        self.setPen(QPen(self.color, 2))
        self.setZValue(1) # stack hodnota - aby bol vrchol "nad" hranou, inak pri kliku na vrchol selektuje hranu
        self.ID = ID
        self.demand = demand
        self.name = name
    
    def get_string(self):
        rows = []
        rows.append(("Node ID", self.ID))
        rows.append(("Node name", self.name))
        rows.append(("Node demand", self.demand))
        rows.append(("X pos", round(self.pos().x(), 2)))
        rows.append(("Y pos", round(self.pos().y() * -1, 2)))
        
        return rows
    
    def set_center(self):
        self.color = QColor("green")
        self.setBrush(QBrush(self.color))
    
    def set_default(self):
        self.color = QColor("black")
        self.setBrush(QBrush(self.color))
        self.setPen(QPen(self.color, 2))
    
    def select(self):
        self.setPen(QPen(QColor("red"), 1.2))
    
    def deselect(self):
        self.setPen(QPen(self.color, 2))