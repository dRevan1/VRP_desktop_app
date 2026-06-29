from PyQt6.QtWidgets import QGraphicsView, QMenu, QInputDialog
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QLineF, pyqtSignal, QPointF, Qt
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
    from_node: Node = None
    
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
        self.graph_change.emit(True) 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # API na backend v app - vyskúša pridať hranu, ak sa vráti none, tak sa nepridá, ale stále zachováme vybraný počiatočný vrchol, v tomto prípade to znamená buď pridávanie hrany
    # s rovnakým začiatočným a koncovým vrcholom, alebo medzi vrcholy, kde už hrana existuje, inak hranu pridá do scény a nastaví vybranú na None - samotné pridanie
    # do štruktúr je v app v "add_edge" metóde
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
    def add_edge(self, _from, to):
        new_edge = self.app.add_edge(_from, to)
        if new_edge is not None:
            self.scene().addItem(new_edge)
            self.item_info.emit([])
            self.from_node = None
            self.graph_change.emit(True)
    #----------------------------------------------------------------------------------------------------------
    # otvorí dialógové okno na zmenu mena vrchola a aktualizuje panel, keďže vrchol je stále vybraný "selected"
    #----------------------------------------------------------------------------------------------------------       
    def rename_node(self, ID):
        node = self.app.graph.nodes[self.app.graph.node_ID_map[ID]]
        new_name, ok = QInputDialog.getText(self, "Rename Node", "Node name:", text=node.name)
        if ok and new_name:
            node.name = new_name
            self.item_info.emit(node.get_string())
            self.graph_change.emit(True) 
    #----------------------------------------------------------------------
    # otvorí dialógové okno na zmenu požiadavky vrchola a aktualizuje panel
    #----------------------------------------------------------------------
    def set_demand(self, ID):
        node = self.app.graph.nodes[self.app.graph.node_ID_map[ID]]
        new_demand, ok = QInputDialog.getInt(self, "Set demand", "Node demand:", value=node.demand, min=0)
        if ok and new_demand:
            node.demand = new_demand
            self.item_info.emit(node.get_string())
            self.graph_change.emit(True)
    #------------------------------------------------------------------------------------------------------------
    # metóda získa list hrán a prioritný front ich ID pre mazanie v "app", potom ich odstráni zo scény, aj vrchol
    #------------------------------------------------------------------------------------------------------------
    def delete_node(self, node: Node):
        edge_list, prior_q = self.app.get_nodes_edges(node)
        for edge in edge_list:
            self.scene().removeItem(edge)
        self.app.remove_node(node, prior_q)
        self.scene().removeItem(node)
        self.item_info.emit([])
    #--------------------------------------------------------------
    # otvorí dialógové okno na zmenu ceny hrany a aktualizuje panel
    #--------------------------------------------------------------
    def set_cost(self, ID):
        edge = self.app.graph.edges[self.app.graph.edge_ID_map[ID]]
        new_cost, ok = QInputDialog.getDouble(self, "Set edge cost", "Edge cost:", value=edge.cost, min=0.0, decimals=2)
        if ok and new_cost:
            edge.cost = new_cost
            edge.label.setPlainText(str(round(edge.cost, 2)))
            self.item_info.emit(edge.get_string())
            self.graph_change.emit(True)
    #-------------------------------
    # zavolá odstránenie hrany v app
    #-------------------------------
    def delete_edge(self, edge: Edge):
        index = self.app.graph.edge_ID_map[edge.ID]
        self.app.remove_edge(edge)
        self.app.update_edge_IDs(index)
        self.scene().removeItem(edge)
        self.graph_change.emit(True) 
        self.item_info.emit([])
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
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # táto metóda spravuje klikacie akcie - keď sa klikne do grafu tak podľa vybraného nástroja a podľa ostatných vlajok sa spravuje akcia
    # pri kurzore sa označujú a odznačujú prvky podľa oblasti kurzora, pri vrcholoch sa pridávajú vrcholy a pri hranách sa vyberá počiatočný alebo koncový vrchol hrany a pridáva sa
    # pri kliknutí pravým tlačidlom na prvok sa zobrazí drop down menu na zmeny - napríklad cena hrany, meno vrchola, nastavenie vrchola ako centrum atd.
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        elif self.app.selected_menu_tool == 1 and event.button() == Qt.MouseButton.LeftButton:
            self.add_node(mouse_pos)      
        elif self.app.selected_menu_tool == 2 and event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            if not isinstance(item, Node) or (self.from_node is not None and self.from_node.ID == item.ID):
                super().mousePressEvent(event)
                return
            else:
                if self.from_node is None:
                    self.from_node = item
                    self.item_info.emit([("Selected start: ", self.from_node.ID)])
                else:
                    self.add_edge(self.from_node.ID, item.ID)
            
        super().mousePressEvent(event)
    #--------------------------------------------------------------------------------------
    # event na kontext menu - keď sa pravým tlačidlom klikne na vrchol/hranu - zoznam akcií
    #--------------------------------------------------------------------------------------
    def contextMenuEvent(self, event):
        if self.app.selected_menu_tool != 0:
            return
        
        item = self.itemAt(event.pos())      
        if isinstance(item, Node):
            menu = QMenu(self)
            edit_node_action = menu.addAction("Rename")
            edit_demand_action = menu.addAction("Set demand")
            edit_center_action = menu.addAction("Set as center")
            delete_node_action = menu.addAction("Delete")
            action = menu.exec(event.globalPos())
            
            if action == edit_node_action:
                self.rename_node(item.ID)
            elif action == edit_demand_action:
                self.set_demand(item.ID)
            elif action == edit_center_action:
                self.app.set_center(item.ID)
                self.graph_change.emit(True) 
            elif action == delete_node_action:
                self.delete_node(item)
        elif isinstance(item, Edge):
            menu = QMenu(self)
            edit_edge_action = menu.addAction("Set cost")
            delete_edge_action = menu.addAction("Delete")
            action = menu.exec(event.globalPos())
            
            if action == edit_edge_action:
                self.set_cost(item.ID)    
            elif action == delete_edge_action:
                self.delete_edge(item)
        else:
            return
                
        return super().contextMenuEvent(event)