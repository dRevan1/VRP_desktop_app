from PyQt6.QtWidgets import QGraphicsView, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QCursor, QPixmap
from PyQt6.QtCore import QLineF, pyqtSignal, Qt
from app import App

#---------------------------------------------------------------------------------------------
# táto trieda obsahuje okno s grafom a mriežkou (+ osi), stará sa o vykresľovanie v tomto okne
#---------------------------------------------------------------------------------------------
class Graph_view(QGraphicsView):
    grid_size = 25
    scale_step = 5
    zoom_in_factor = 1.15
    zoom_out_factor = 1 / zoom_in_factor
    mouse_coords = pyqtSignal(float, float)
    node_radius = 8.0
    
    def __init__(self, scene, app: App):
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # drag posun grafu
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.centerOn(0, 0)
        self.app = app
        
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.drawEllipse(2, 2, 16, 16)
        painter.end()
        self.setCursor(QCursor(pixmap, 10, 10))
    
    def draw_network(self):
        for edge in self.app.graph.edges:
            _from = self.app.graph.nodes[edge._from - 1]
            to = self.app.graph.nodes[edge.to - 1]
            self.scene().addLine(_from.posX, _from.posY * -1, to.posX, to.posY * -1, QPen(QColor("black"), 0.8))
        for node in self.app.graph.nodes:
            if node.ID == self.app.graph.center:
                self.scene().addEllipse(node.posX - (self.node_radius / 2), (node.posY + (self.node_radius / 2)) * -1, 
                                        self.node_radius, self.node_radius, QPen(QColor("green"), 2), QBrush(QColor("green")))
                continue       
            self.scene().addEllipse(node.posX - (self.node_radius / 2), (node.posY + (self.node_radius / 2)) * -1, 
                                    self.node_radius, self.node_radius, QPen(QColor("black"), 2), QBrush(QColor("black")))
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
        x, y = left, top
        painter.setPen(QPen(QColor('lightgray'), 1))
        while x < rect.right():
            painter.drawLine(QLineF(x, rect.top(), x, rect.bottom()))
            x += self.grid_size
        while y < rect.bottom():
            painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
            y += self.grid_size
    #------------------------------
    # aktualizuje súradnice kurzora
    #------------------------------
    def mouseMoveEvent(self, event):
        mouse_pos = self.mapToScene(event.pos())
        self.mouse_coords.emit(mouse_pos.x(), mouse_pos.y())
        super().mouseMoveEvent(event)     
    #----------------------------------------
    # využíva metódu z QGraphicsView na zoom
    # override handleru
    #----------------------------------------
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)