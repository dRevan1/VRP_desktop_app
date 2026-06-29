from PyQt6.QtWidgets import QToolBar, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QGraphicsScene, QFormLayout 
from PyQt6.QtWidgets import QLabel, QGridLayout, QFileDialog, QMessageBox, QGraphicsView, QPushButton, QInputDialog
from PyQt6.QtGui import QAction, QActionGroup, QColor, QFont
from PyQt6.QtCore import Qt
from graph_view import Graph_view
from graph_scale_view import Graph_scale_view
from coords_view import Coords_view
from app import App


class Main_window(QMainWindow): 
    def __init__(self, app: App):
        super().__init__()
        self.setWindowTitle("Vehicle Routing Problem - Graph Editor")
        self.app = app
        self.init_layout()
      
      
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # metóda inicializuje layout - dá jednotlivé časti (widget) do stĺpca, ktorý predstavuje najvyššiu úroveň hierarchie rozdelenia obrazovky
    # v rámci QMainWindow je menu bar a tool bar, teda tie nie sú v layoute
    # layout obsahuje 2 riadky, v prvom je naľavo panel s info, napríklad súradnice kurzora/vybraného vrchola atd., vpravo je graf a v druhom riadku je konzola na výpisy
    # graf sa skladá zo samostatného layoutu, kde sú v mriežke 3 objekty - samotný plot grafu a mierka/pravítko (graph_scale_veiw) vľavo a pod ním ako samostatné objekty
    # mierka ukazuje od dolného ľavého rohu súradnice v určených intervaloch, dá sa zmeniť v kóde na iný "krok"
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def init_layout(self):
        central = QWidget()  # centrálny widget - QMainWindow už má layout, treba takto a do neho dať layout
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central) # hlavný stĺpec, na vrchu hierarchie rozloženia
        central.setLayout(main_layout)
        self.resize(1000, 800) # rozmery po spustení aplikácie
        
        #inicializácia layoutu
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        col1 = QVBoxLayout()
        main_layout.addLayout(row1, 80) # riadky aj s pomerom priestoru, ktorý zaberú (na výšku)
        main_layout.addLayout(row2, 20)
        self.panel_widget = QWidget() # info panel vľavo
        self.info_panel = QFormLayout(self.panel_widget)
        self.update_info_panel([])
        self.vrp_button = QPushButton()
        self.vrp_button.setText("VRP")
        self.vrp_button.clicked.connect(self.run_VRP)
        self.refresh_button = QPushButton()
        self.refresh_button.setText("Refresh")
        self.refresh_button.clicked.connect(self.refresh_view)
        self.capacity_button = QPushButton()
        self.capacity_button.setText("Set vehicle capacity")
        self.capacity_button.clicked.connect(self.set_capacity)
        
        # inicializácia grafu a riadkov
        self.graph_widget = QWidget() # samostatný widget pre grid layout grafu a mierok/osí
        self.graph_layout = QGridLayout(self.graph_widget)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, -2_000_000, 2_000_000, 2_000_000)
        self.graph_view = Graph_view(self.scene, self.app)
        self.coords_view = Coords_view(self.graph_view)
        self.h_scale = Graph_scale_view(self.graph_view) # horizontálna mierka/pravítko
        self.v_scale = Graph_scale_view(self.graph_view, True) # vertikálna mierka/pravítko
        self.graph_layout.addWidget(self.h_scale, 1, 1)
        self.graph_layout.addWidget(self.v_scale, 0, 0)
        self.graph_layout.addWidget(self.graph_view, 0, 1)
        self.graph_view.horizontalScrollBar().valueChanged.connect(self.h_scale.update)
        self.graph_view.horizontalScrollBar().valueChanged.connect(self.v_scale.update)
        self.graph_view.verticalScrollBar().valueChanged.connect(self.h_scale.update)
        self.graph_view.verticalScrollBar().valueChanged.connect(self.v_scale.update)
        self.graph_view.graph_change.connect(self.get_graph_change)
        self.graph_view.item_info.connect(self.update_info_panel)
        
        col1.addWidget(self.vrp_button, 1)
        col1.addWidget(self.refresh_button, 1)
        col1.addWidget(self.capacity_button, 1)
        col1.addWidget(self.panel_widget, 9)
        col1.addWidget(self.coords_view, 1)
        row1.addLayout(col1, 1)
        row1.addWidget(self.graph_widget, 14)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        font = QFont("Arial", 12, 15)
        self.console.setFont(font)
        row2.addWidget(self.console)
        
        # inicializácia menu
        self.menu_bar = self.menuBar().addMenu("File")
        self.new_file = self.menu_bar.addAction("New File...")
        self.open_file = self.menu_bar.addAction("Open File...")
        self.save_file = self.menu_bar.addAction("Save File...")
        self.new_file.triggered.connect(self.new_file_action)
        self.open_file.triggered.connect(self.open_file_action)
        self.save_file.triggered.connect(self.save_file_action)
        self.save_file.setEnabled(False)
        
        # inicializácia tool bar
        self.toolbar = QToolBar(self)
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(self.toolbar)
        self.tool_group = QActionGroup(self)
        self.tool_group.setExclusive(True)
        
        self.cursor_action = QAction("Cursor", self) # nástroj pre kurzor, na vyberanie umiestnených vrcholov, hrán atd.
        self.cursor_action.setToolTip("Cursor")
        self.cursor_action.setCheckable(True)
        self.cursor_action.triggered.connect(self.select_cursor)
        self.cursor_action.setChecked(True)
        
        self.add_node_action = QAction("Node", self) # nástroj na pridanie vrchola - keď je zakliknutý môžu sa do grafu pokladať vrcholy
        self.add_node_action.setToolTip("Place a node")
        self.add_node_action.setCheckable(True)
        self.add_node_action.triggered.connect(self.select_add_node)
        
        self.add_edge_action = QAction("Edge", self) # nástroj na pridanie hrany - keď je zakliknutý môžu sa do grafu pridávať hrany
        self.add_edge_action.setToolTip("Place an edge")
        self.add_edge_action.setCheckable(True)
        self.add_edge_action.triggered.connect(self.select_add_edge)
        
        self.tool_group.addAction(self.cursor_action)
        self.tool_group.addAction(self.add_node_action)
        self.tool_group.addAction(self.add_edge_action)
        self.toolbar.addAction(self.cursor_action)
        self.toolbar.addAction(self.add_node_action)
        self.toolbar.addAction(self.add_edge_action)
    # ///// MENU BAR /////
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # akcia napojená na otvorenie nového súboru z menu, ak je neuložená práca, najskôr sa spýta užívateľa, či chce projekt uložiť, potom sa resetujú štruktúry a tým sa vytvorí nový "projekt"
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    def new_file_action(self):
        if self.app.graph_change:
            reply = QMessageBox.warning(self, "Save project", "Do you want to save the project before creating a new one?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.Yes)
            if (reply == QMessageBox.StandardButton.Yes):
                self.save_file_action()
        
        self.app.project_name = "New project"
        self.graph_view.reset_canvas()
        self.app.graph.init_structures()
        self.app.graph_change = False
        self.update_info_panel([])
        self.save_file.setEnabled(False)
        self.console.clear()
        self.app.refreshed = True
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    # akcia napojená na otvorenie súboru, ak sú neuložené zmeny, najskôr sa spýta užívateľa, či chce uložiť projekt, potom sa otvorí QFileDialog na uloženie
    # na konci sa aktualizuje názov otvoreného súbora pre výpis v aplikácii
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    def open_file_action(self):
        if self.app.graph_change:
            reply = QMessageBox.warning(self, "Save project", "Do you want to save the project before opening a new one?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.Yes)
            if (reply == QMessageBox.StandardButton.Yes):
                self.save_file_action()
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File - Graph Network",
            "",
            "Text Files (*.txt);;All Files (*)"
        )    
        if file_path: 
            self.app.project_name = file_path.split('/')[-1].split('.')[0] # názov otvoreného projektu bude zobrazený v aplikácii - spraví sa split podľa / a potom podľa .
            self.graph_view.reset_canvas()
            self.app.load_new_network(file_path)
            self.save_file.setEnabled(True)
            self.app.graph_change = False
            self.update_info_panel([])
            self.graph_view.draw_network()
            self.console.clear()
            self.app.refreshed = True
    #---------------------------------------------------------------------------------------------------
    # akcia napojená na uloženie súbora z menu, spýta sa, či chce užívateľ uložiť aj maticu vzdialeností
    # na konci je info okno, keď sa projekt uložil úspešne
    #---------------------------------------------------------------------------------------------------
    def save_file_action(self):
        reply = QMessageBox.question(self, "Save weights", "Do you want to save edge weights (distance matrix)?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.Yes)
        reply = (reply == QMessageBox.StandardButton.Yes)   
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Text File - Graph Network",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.app.save_network(file_path, reply)
            self.app.graph_change = False
            QMessageBox.information(self, "Project saved", "Your project has been saved successfully.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    # ///// TOOL BAR /////
    #---------------------------------------------------------------------------------------------------------------------------------------
    # tieto akcie sú napojené na zakliknutie nástrojov z tool baru - aktualizujú hodnotu v app, ktorá hovorí, ktorý nástroj je práve zvolený
    #---------------------------------------------------------------------------------------------------------------------------------------
    def select_cursor(self):
        self.app.selected_menu_tool = 0
        self.graph_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.graph_view.from_node = None
  
    def select_add_node(self):
        self.app.selected_menu_tool = 1
        self.graph_view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.graph_view.from_node = None
        if self.graph_view.selected_item is not None:
            self.graph_view.selected_item.deselect()
            self.graph_view.selected_item = None
        self.graph_view.item_info.emit([])   
   
    def select_add_edge(self):
        self.app.selected_menu_tool = 2
        self.graph_view.setDragMode(QGraphicsView.DragMode.NoDrag)
        if self.graph_view.selected_item is not None:
            self.graph_view.selected_item.deselect()
            self.graph_view.selected_item = None
        self.graph_view.item_info.emit([])
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # skontroluje, či sa dá psustiť VRP a ak áno, spustí sa a aktualizuje graf, zároveň vypíše výsledok do konzoly (príkazový riadok) a do "konzoly" / textového poľa v aplikácii
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def run_VRP(self):
        if len(self.app.graph.nodes) == 0:
            QMessageBox.critical(self, "Network empty", "Cannot run VRP, the network is empty!", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        if not self.app.graph.connected:
            QMessageBox.critical(self, "Network disconnected", "Cannot run VRP, the network is disconnected!", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        if self.app.graph.center == 0:
            QMessageBox.critical(self, "No center", "Cannot run VRP, the center is not set!", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        
        if not self.app.refreshed:
            self.refresh_view()
        console_info = self.app.run_VRP()
        for v_edge in self.app.virtual_edges:
            self.graph_view.scene().addItem(v_edge)
        self.update_console(console_info)
        self.app.refreshed = False        
    #--------------------------------------------------------------------------------
    # refresh konzoly a grafu po spustení VRP - vyznačenie ciest a výsledok z konzoly
    #--------------------------------------------------------------------------------
    def refresh_view(self):
        for edge in self.app.graph.edges:
            edge.unmark()
        while len(self.app.virtual_edges) > 0:
            self.graph_view.scene().removeItem(self.app.virtual_edges[-1])
            self.app.virtual_edges.pop(-1)
        
        self.console.clear()
        self.app.refreshed = True
    #-------------------------------------------
    # zmení kapacitu vozidiel cez dialógové okno
    #-------------------------------------------
    def set_capacity(self):
        if not self.app.refreshed:
            return
        new_capacity, ok = QInputDialog.getInt(self, "Set Vehicle Capacity", "Vehicle capacity:", self.app.graph.capacity, 1)
        if ok:
            self.app.graph.capacity = new_capacity
            self.update_info_panel([])
            self.app.graph_change = True
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # aktualizuje info panel - odstráni súčasbé riadky a pridá názov projektu + všetky riadky v liste "fields" vo podobe tuple s názvom poľa a hodnotou (v pôvodnom type)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_info_panel(self, fields: list[tuple]):
        while self.info_panel.rowCount():
            self.info_panel.removeRow(0)
              
        self.info_panel.addRow("Project open:", QLabel(self.app.project_name))
        self.info_panel.addRow("Vehicle capacity:", QLabel(str(self.app.graph.capacity)))
        for row in fields:
            self.info_panel.addRow(row[0] + ": ", QLabel(str(row[1])))
            
    def update_console(self, rows: list):       
        for row in rows:
            self.console.append(row)
    #------------------------------------------------------------------------------------------------------------------
    # override close eventu, pred ukončením aplikácie sa pri neuložených zmenách spýta, či chce užívateľ uložiť projekt
    #------------------------------------------------------------------------------------------------------------------    
    def closeEvent(self, a0):
        if self.app.graph_change:
            reply = QMessageBox.warning(self, "Save project", "Do you want to save the project before exiting?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.Yes)
            if (reply == QMessageBox.StandardButton.Yes):
                self.save_file_action()
        return super().closeEvent(a0)
    
    def get_graph_change(self, change):
        if change:
            self.save_file.setEnabled(True)
            self.app.graph_change = True