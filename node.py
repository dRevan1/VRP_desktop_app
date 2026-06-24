from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QColor, QBrush

class Node(QGraphicsEllipseItem):
    def __init__(self, ID: int, posX: float, posY: float, demand: int, name: str, type: int):
        super().__init__(-8.0 / 2, -8.0 / 2, 8.0, 8.0)
        self.setPos(posX, -posY)
        if type == 0:
            self.setBrush(QBrush(QColor("black")))
            self.setPen(QPen(QColor("black"), 2))
        elif type == 1:
            self.setBrush(QBrush(QColor("green")))
            self.setPen(QPen(QColor("green"), 2))
            
        self.ID = ID
        self.demand = demand
        self.name = name