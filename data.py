from pathlib import Path
import numpy as np

class Data:
    def __init__(self, nodes_path: str, edges_path: str):
        self.nodes = [] # vrcholy
        self.D = [] # matica vzdialeností
        self.capacity: int # kapacita vozidiel
        self.load_data(nodes_path, edges_path)
        
    #
    # načíta údaje z .txt súboru
    # nodes - vrcholy, prvý riadok = počet vrcholov, kapacita vozidiel, mód (0 ak sú súradnice absolútne, neprepočítavajú sa, 1 ak ich treba transformovať)
    #       - ostatné riadky = vrchol ID, súradnica x, súradnica y, požiadavka, názov (string)
    # edges - hrany, prvý riadok = počet hrán, mód (0 ak existuje stĺpec pre ceny, 1 ak neexsituje, vypočíta sa ako euklidovská vzdialenosť medzi vrcholmi)
    #       - ostatné riadky = vrchol z, vrchol do, (optional) cena hrany
    #
    def load_data(self, nodes_path: str, edges_path: str):
        file_path = Path(nodes_path)
        if not file_path.exists():
            print(f"File {nodes_path} for nodes does not exist.")
            return
        file_path = Path(edges_path)
        if not file_path.exists():
            print(f"File {edges_path} for edges does not exist.")
            return
            
        with open(nodes_path, 'r') as f:
            for line in f:
                x, y = map(float, line.strip().split(','))
                self.nodes.append(np.array([x, y]))

        with open(edges_path, 'r') as f:
            for line in f:
                row = list(map(int, line.strip().split(',')))
                self.D.append(row)