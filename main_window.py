from PyQt6.QtWidgets import QToolBar, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QGraphicsScene, QFormLayout, QLabel, QGridLayout
from PyQt6.QtGui import QAction, QActionGroup, QIcon
from PyQt6.QtCore import Qt
from graph_view import Graph_view
from graph_scale_view import Graph_scale_view
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
        main_layout.addLayout(row1, 80) # riadky aj s pomerom priestoru, ktorý zaberú (na výšku)
        main_layout.addLayout(row2, 20)
        self.panel_widget = QWidget() # info panel vľavo
        self.info_panel = QFormLayout(self.panel_widget)
        self.info_panel.addRow("Node ID:", QLabel("5"))
        self.info_panel.addRow("X:", QLabel("120"))
        self.info_panel.addRow("Y:", QLabel("340"))
        
        # inicializácia grafu a riadkov
        self.graph_widget = QWidget() # samostatný widget pre grid layout grafu a mierok/osí
        self.graph_layout = QGridLayout(self.graph_widget)
        self.scene = QGraphicsScene()
        self.graph_view = Graph_view(self.scene)
        self.h_scale = Graph_scale_view(self.graph_view) # horizontálna mierka/pravítko
        self.v_scale = Graph_scale_view(self.graph_view, True) # vertikálna mierka/pravítko
        self.graph_layout.addWidget(self.h_scale, 1, 1)
        self.graph_layout.addWidget(self.v_scale, 0, 0)
        self.graph_layout.addWidget(self.graph_view, 0, 1)
        
        row1.addWidget(self.panel_widget, 1) # pridanie prvkov do riadkov
        row1.addWidget(self.graph_widget, 14)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        row2.addWidget(self.console)
        
        # inicializácia menu
        self.menu_bar = self.menuBar().addMenu("File")
        self.menu_bar.addAction("New File...")
        self.menu_bar.addAction("Open File...")
        self.menu_bar.addAction("Save File...")
        
        # inicializácia tool bar
        self.toolbar = QToolBar(self)
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(self.toolbar)
        self.tool_group = QActionGroup(self)
        self.tool_group.setExclusive(True)
        
        self.cursor_action = QAction(QIcon("icons/cursor.png"), "Cursor", self) # nástroj pre kurzor, na vyberanie umiestnených vrcholov, hrán atd.
        self.cursor_action.setToolTip("Cursor")
        self.cursor_action.setCheckable(True)
        self.cursor_action.setChecked(True)
        
        self.add_node_action = QAction(QIcon("icons/node.png"), "Node", self) # nástroj na pridanie vrchola - keď je zakliknutý môžu sa do grafu pokladať vrcholy
        self.add_node_action.setToolTip("Place a node")
        self.add_node_action.setCheckable(True)
        
        self.add_edge_action = QAction(QIcon("icons/edge.png"), "Edge", self) # nástroj na pridanie hrany - keď je zakliknutý môžu sa do grafu pridávať hrany
        self.add_edge_action.setToolTip("Place an edge")
        self.add_edge_action.setCheckable(True)
        
        self.tool_group.addAction(self.cursor_action)
        self.tool_group.addAction(self.add_node_action)
        self.tool_group.addAction(self.add_edge_action)
        self.toolbar.addAction(self.cursor_action)
        self.toolbar.addAction(self.add_node_action)
        self.toolbar.addAction(self.add_edge_action)