from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import QLineF, Qt

#---------------------------------------------------------------------------------------------
# táto trieda obsahuje okno s grafom a mriežkou (+ osi), stará sa o vykresľovanie v tomto okne
#---------------------------------------------------------------------------------------------
class Graph_view(QGraphicsView):
    grid_size = 25
    scale_step = 5
    zoom_in_factor = 1.15
    zoom_out_factor = 1 / zoom_in_factor
    
    def __init__(self, scene):
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # drag posun grafu
        self.centerOn(0, 0)
    
    
    #----------------------------------------------------------------------------------------------------------------
    # táto metóda vykresľuje mriežku, teda pozadie okna
    # postupne sa od začiatku prejde horizontálne na koniec a vykreslia sa hodnoty s daným krokom, rovnako vertikálne
    # override handleru
    #----------------------------------------------------------------------------------------------------------------
    def drawBackground(self, painter: QPainter, rect):
        super().drawBackground(painter, rect)
        left = float(rect.left()) - (float(rect.left()) % self.grid_size)
        top = float(rect.top()) - (float(rect.top()) % self.grid_size)
        
        # vykreslenie mriežky
        x = left
        y = top
        painter.setPen(QPen(QColor('lightgray'), 1))
        while x < rect.right():
            painter.drawLine(QLineF(x, rect.top(), x, rect.bottom()))
            x += self.grid_size
        while y < rect.bottom():
            painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
            y += self.grid_size
    #----------------------------------------
    # využíva metódu z QGraphicsView na zoom
    # override handleru
    #----------------------------------------
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)