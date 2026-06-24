from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import QLineF

class Edge(QGraphicsLineItem):
    def __init__(self, ID: int, _from: int, _fromX: float, _fromY: float, to: int, toX: float, toY: float, cost: int):
        super().__init__()
        self.setLine(_fromX, _fromY, toX, toY)
        self.setPen(QPen(QColor("black"), 0.8))
        self.ID = ID
        self._from = _from
        self.to = to
        self.cost = cost