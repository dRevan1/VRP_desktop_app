from pathlib import Path
import node
import edge

class Data:
    def __init__(self, nodes_path: str, edges_path: str):
        self.nodes: list[node.Node] = []  # vrcholy
        self.edges: list[edge.Edge] = [] # hrany
        self.capacity: int # kapacita vozidiel
        self.load_data(nodes_path, edges_path)
        
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    # načíta údaje z .txt súboru
    # nodes - vrcholy, prvý riadok = počet vrcholov, kapacita vozidiel, mód (0 ak sú súradnice absolútne, neprepočítavajú sa, 1 ak ich treba transformovať)
    #       - ostatné riadky = vrchol ID, súradnica x, súradnica y, požiadavka, názov (string)
    # edges - hrany, prvý riadok = počet hrán, mód (0 ak existuje stĺpec pre ceny, 1 ak neexsituje, vypočíta sa ako euklidovská vzdialenosť medzi vrcholmi)
    #       - ostatné riadky - vrchol z, vrchol do, (optional) cena
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    def load_data(self, nodes_path: str, edges_path: str):
        # kontrola existencie súborov
        file_path = Path(nodes_path)
        if not file_path.exists():
            print(f"File {nodes_path} for nodes does not exist.")
            return
        file_path = Path(edges_path)
        if not file_path.exists():
            print(f"File {edges_path} for edges does not exist.")
            return
        
        # načítanie vrcholov
        with open(nodes_path, 'r') as f:
            n, self.capacity, center, mode = map(int, f.readline().split())
            for i in range(1, n+1):
                id, x, y, demand, name = f.readline().split()
                _type = 0 if i != center else 1
                self.nodes.append(node.Node(id, x, y, demand, name, _type))
                
        # načítanie hrán
        with open(edges_path, 'r') as f:
            n, mode = map(int, f.readline().split())
            for i in range(1, n+1):
                _from = to = cost = -1
                if mode == 0:
                    _from, to, cost = f.readline().split()
                elif mode == 1:
                    _from, to = f.readline().split()
                    
                self.edges.append(edge.Edge(i-1, _from, to, cost))    