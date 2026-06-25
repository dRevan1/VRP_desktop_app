from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen, QColor

class Virtual_edge(QGraphicsLineItem):
    def __init__(self, ID: int, _from: int, _fromX: float, _fromY: float, to: int, toX: float, toY: float, cost: int, path: list[int]):
        super().__init__()
        self.setLine(_fromX, _fromY, toX, toY)
        self.color = QColor("black")
        self.setPen(QPen(self.color, 0.8))
        self.setZValue(0) # stack hodnota - aby bola hrana "pod" vrcholom, inak pri kliku na vrchol selektuje hranu
        self.ID = ID
        self._from = _from
        self.to = to
        self.cost = cost
        self.path = path
        
    def get_string(self):
        rows = []
        rows.append(("Edge ID", self.ID))
        rows.append(("From", self._from))
        rows.append(("To", self.to))
        path_str = [str(node) + ", " for node in self.path]
        rows.append(("Path", path_str))
        rows.append(("Cost", self.cost))
        
        return rows
    
    def select(self):
        self.setPen(QPen(QColor("red"), 0.8))
    
    def deselect(self):
        self.setPen(QPen(self.color, 0.8))
        
    def mark(self, color: QColor):
        self.color = color
        self.setPen(QPen(self.color, 0.8))
        
    def unmark(self):
        self.color = self.color = QColor("black")
        self.setPen(QPen(self.color, 0.8))