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
        point = 0
        step = 0
        
        if self.vertical:
            while point < self.height():
                if step % self.view.scale_step == 0:
                    painter.drawText(2, self.height() - (int(point)), str(int(point))) # keďže súradnice začínajú hore vľavo, treba kresliť na bottom - offset, alebo ísť od height do 0
                    step = 0
                point += self.view.grid_size
                step += 1
        else:
            while point < self.width():
                if step % self.view.scale_step == 0:
                    painter.drawText((int(point) + 2), 10, str(int(point)))
                    step = 0
                point += self.view.grid_size
                step += 1
                
        painter.end()