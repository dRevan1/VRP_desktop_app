from pathlib import Path
import VRP_graph as VRP
import numpy as np
from math import floor

class Data_handler:    
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    # načíta údaje z .txt súboru a uloží ich do štruktúr
    # nodes - vrcholy, prvý riadok = počet vrcholov, kapacita vozidiel, mód (0 ak sú súradnice absolútne, neprepočítavajú sa, 1 ak ich treba transformovať)
    #       - ostatné riadky = vrchol ID, súradnica x, súradnica y, požiadavka, názov (string)
    # edges - hrany, prvý riadok = počet hrán, mód (0 ak existuje stĺpec pre ceny, 1 ak neexsituje, vypočíta sa ako euklidovská vzdialenosť medzi vrcholmi)
    #       - ostatné riadky - vrchol z, vrchol do, (optional) cena
    # D - matica vzdialeností, prvý riadok je počet riadkov matice, ostatné sú jednotlivé vzdialenosti v riadku
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    def load_data(self, network_path: str, graph: VRP.Graph):
        # kontrola existencie súborov
        file_path = Path(network_path)
        if not file_path.exists():
            print(f"File {network_path} for network does not exist.")
            return
        
        # načítanie vrcholov
        with open(file_path, 'r') as f:
            n, graph.capacity, graph.center, graph.mode_nodes = map(int, f.readline().split())
            for i in range(n):
                id, x, y, demand, name = f.readline().split()
                id, x, y, demand = int(id), float(x), float(y), int(demand)
                _type = 0 if id != graph.center else 1
                graph.nodes.append(VRP.Node(id, x, y, demand, name, _type))
            
            graph.edges_star.extend([] for node in range(n)) # inicializácia hviezdy - n prázdnych listov v edges_star
            for i in range(n): # inicializácia matice vzdialeností - n * n s hodnotou -1
                row = [-1 for col in range(n)]
                row[i] = 0
                graph.D.append(row)
            
            # načítanie hrán
            n, graph.mode_edges = map(int, f.readline().split())
            id = 0
            for i in range(n):
                _from = to = cost = -1
                if graph.mode_edges == 0: # ceny sú zadané
                    _from, to, cost = f.readline().split()
                elif graph.mode_edges == 1: # ceny sa počítajú L2 normou
                    _from, to = map(int, f.readline().split())
                    from_np = np.array([graph.nodes[_from - 1].posX, graph.nodes[_from - 1].posY])
                    to_np = np.array([graph.nodes[to - 1].posX, graph.nodes[to - 1].posY])
                    cost = floor(np.linalg.norm(from_np - to_np))   
                
                _from, to, cost = int(_from), int(to), float(cost)
                graph.edges.append(VRP.Edge(id, _from, to, cost))
                graph.edges_star[_from - 1].append(VRP.Edge(id, _from, to, cost)) # vrcholy sú indexované od 1 - teda index v programe bude i - 1
                id += 1
                graph.edges_star[to - 1].append(VRP.Edge(id, to, _from, cost))
                id += 1
                graph.D[_from - 1][to - 1] = graph.D[to - 1][_from - 1] = cost # doplnenie existujúcich hrán do matice vzdialeností
                
            # načítanie (optional) matice vzdialeností
            n = int(f.readline())
            for i in range(n):
                line = f.readline()
                dist = list(map(float, line.split()))
                graph.D[i] = dist
    #-------------------------------------------------------------------
    # uloží údaje do .txt súboru s rovnakým formátom, ako pri načítavaní
    #-------------------------------------------------------------------
    def save_data(self, network_path: str, save_dist, graph: VRP):
        with open(network_path, 'w') as f:
            # zápis vrcholov
            control_str = [len(graph.nodes), graph.capacity, graph.center, graph.mode_nodes] # prvý riadok pre vrcholy
            f.write(' '.join(map(str, control_str)) + '\n')
            for node in graph.nodes:
                node_str = [node.ID, node.posX, node.posY, node.demand, node.name]
                f.write(' '.join(map(str, node_str)) + '\n')
                
            # zápis hrán
            control_str = [len(graph.edges), graph.mode_edges] # prvý riadok pre hrany
            f.write(' '.join(map(str, control_str)) + '\n')
            for edge in graph.edges:
                edge_str = [edge._from, edge.to]
                if graph.mode_edges == 0:
                    edge_str.append(edge.cost) 
                f.write(' '.join(map(str, edge_str)) + '\n')
                
            # zápis (optional) matice vzdialeností
            if save_dist:
                f.write(str(len(graph.D)) + '\n')
                for row in graph.D:
                    f.write(' '.join(map(str, row)) + '\n')
                return
            
            f.write(str(0) + '\n')