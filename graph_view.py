from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import QLineF, pyqtSignal, QPointF
from app import App
from node import Node
from edge import Edge

#---------------------------------------------------------------------------------------------
# táto trieda obsahuje okno s grafom a mriežkou (+ osi), stará sa o vykresľovanie v tomto okne
#---------------------------------------------------------------------------------------------
class Graph_view(QGraphicsView):
    grid_size = 25
    scale_step = 5
    zoom_in_factor = 1.15
    zoom_out_factor = 1 / zoom_in_factor
    mouse_coords = pyqtSignal(float, float)
    graph_change = pyqtSignal(bool) # flag či bola vykonaná nejaká zmena - pridanie/vymazanie vrchola/hrany atd., podľa toho sa pýta užívateľa pri rôznych akciách, či chce uložiť súbor
    item_info = pyqtSignal(list)
    selected_item = None
    
    def __init__(self, scene, app: App):
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # drag posun grafu
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.centerOn(0, 0)
        self.app = app
    
    
    #-------------------------------------------------
    # do scény pridá hrany a vrcholy, tým sa vykreslia
    #-------------------------------------------------
    def draw_network(self):
        for edge in self.app.graph.edges:
            self.scene().addItem(edge)
        for node in self.app.graph.nodes:    
            self.scene().addItem(node)
    #--------------------------------------------------------------------------------------------
    # odstráni všetky prvky z grafu - po vytvorení nového projektu alebo pri načítaní novej siete
    #--------------------------------------------------------------------------------------------
    def reset_canvas(self):
        self.scene().clear()
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
    #------------------------------------------------------------------------------------------------------------------------------------
    # API na backend v app - po pridaní vrchola sa zavolá metóda v app, aby sa pridal do štruktúr, v tejto metóde sa potom pridá do grafu
    #------------------------------------------------------------------------------------------------------------------------------------
    def add_node(self, mouse_pos: QPointF):
        self.scene().addItem(self.app.add_node(mouse_pos.x(), mouse_pos.y()))
              
    def add_edge(self):
        self.app.remove_edge()
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
    #
    #
    #
    def mousePressEvent(self, event):
        mouse_pos = self.mapToScene(event.pos())
        if self.app.selected_menu_tool == 0:
            item = self.itemAt(event.pos())
            if isinstance(item, Node) or isinstance(item, Edge):
                info = item.get_string()
                if self.selected_item is not None:
                    self.selected_item.deselect()
                item.select()
                self.selected_item = item
                self.item_info.emit(info)
            else:
                self.item_info.emit([])
                if self.selected_item is not None:
                    self.selected_item.deselect()
                self.selected_item = None
        elif self.app.selected_menu_tool == 1:
            self.add_node(mouse_pos)
            self.graph_change.emit(True)
        elif self.app.selected_menu_tool == 2:
            self.add_edge(mouse_pos)
            self.graph_change.emit(True)
        super().mousePressEvent(event)