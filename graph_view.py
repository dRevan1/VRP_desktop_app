from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QLineF

#---------------------------------------------------------------------------------------------
# táto trieda obsahuje okno s grafom a mriežkou (+ osi), stará sa o vykresľovanie v tomto okne
#---------------------------------------------------------------------------------------------
class Graph_view(QGraphicsView):
    grid_size = 25
    scale_step = 5
    
    
    #----------------------------------------------------------------------------------------------------------------
    # táto metóda vykresľuje mriežku, teda pozadie okna
    # postupne sa od začiatku prejde horizontálne na koniec a vykreslia sa hodnoty s daným krokom, rovnako vertikálne
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