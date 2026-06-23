from PyQt6.QtWidgets import QWidget
from graph_view import Graph_view
from PyQt6.QtGui import QPainter, QPen, QColor

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# táto trieda obsahuje osu/mierku/pravítko, ktoré patrí k plotu grafu, pri inicializácii na nastaví, či je inštancia horizontálna alebo vertikálna mierka
# trieda obsahuje aj referenciu na graph_view, teda na samotný plot grafu, aby sa mohli správne nastavovať hodnoty, napríklad pri pohybe a priblížení
#--------------------------------------------------------------------------------------------------------------------------------------------------------
class Graph_scale_view(QWidget):
    def __init__(self, view: Graph_view, vertical: bool = False):
        super().__init__()
        self.vertical = vertical
        self.view = view
        if vertical: # nastavenie fixného druhého rozmeru podľa orientácie mierky
            self.setFixedWidth(40)
        else:
            self.setFixedHeight(20)


    #----------------------------------------------------------------------------------------------------------------------------------
    # metóda robí vykreslenie hodnôt, podobne ako graph_view ide postupne od svojho začiatku až po koniec a s krokom vykresľuje hodnoty
    #----------------------------------------------------------------------------------------------------------------------------------
    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor('black'), 1)
        painter.setPen(pen)
        
        if self.vertical:
            for screen_y in range(0, self.height(), self.view.grid_size * self.view.scale_step):
                scene_y = self.view.mapToScene(0, screen_y).y() * -1 # scene je súradnica, ktorá sa vykreslí (na mierke v aplikácii)
                painter.drawText(2, screen_y, str(int(scene_y)))
        else:
            for screen_x in range(0, self.width(), self.view.grid_size * self.view.scale_step):
                scene_x = self.view.mapToScene(screen_x, 0).x()
                painter.drawText(screen_x, 10, str(int(scene_x)))
                
        painter.end()