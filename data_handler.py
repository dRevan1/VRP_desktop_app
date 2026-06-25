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
            n, graph.capacity, graph.center = map(int, f.readline().split())
            for i in range(n):
                id, x, y, demand, name = f.readline().split()
                id, x, y, demand = int(id), float(x), float(y), int(demand)
                _type = 0 if id != graph.center else 1
                graph.nodes.append(VRP.Node(id, x, y, demand, name, _type))
                graph.ID_map[id] = i
                if id > graph.next_ID:
                    graph.next_ID = id
            graph.next_ID += 1
            
            graph.edges_star.extend([] for node in range(n)) # inicializácia hviezdy - n prázdnych listov v edges_star
            for i in range(n): # inicializácia matice vzdialeností - n * n s hodnotou -1
                row = [-1 for col in range(n)]
                row[i] = 0
                graph.D.append(row)
            
            # načítanie hrán
            n, graph.mode_edges = map(int, f.readline().split())
            id = 0
            for i in range(n):
                _from_ID = to_ID = cost = -1
                if graph.mode_edges == 0: # ceny sú zadané
                    _from_ID, to_ID, cost = f.readline().split()
                    _from, to = graph.ID_map[_from_ID], graph.ID_map[to_ID] # index cez ID z mapy
                elif graph.mode_edges == 1: # ceny sa počítajú L2 normou
                    _from_ID, to_ID = map(int, f.readline().split())
                    _from, to = graph.ID_map[_from_ID], graph.ID_map[to_ID]
                    from_np = np.array([graph.nodes[_from].pos().x(), graph.nodes[_from].pos().y()])
                    to_np = np.array([graph.nodes[to].pos().x(), graph.nodes[to].pos().y()])
                    cost = floor(np.linalg.norm(from_np - to_np))   
                
                _from_ID, to_ID, cost = int(_from_ID), int(to_ID), float(cost)
                _from_pos = graph.nodes[_from].pos()
                to_pos = graph.nodes[to].pos()
                graph.edges.append(VRP.Edge(id, _from_ID, _from_pos.x(), _from_pos.y(), to_ID, to_pos.x(), to_pos.y(), cost))
                graph.edges_star[_from].append(VRP.Edge(id, _from_ID, _from_pos.x(), _from_pos.y(), to_ID, to_pos.x(), to_pos.y(), cost)) # vrcholy majú ID od 1 vyššie
                graph.edges_star[to].append(VRP.Edge(id, to_ID, to_pos.x(), to_pos.y(), _from_ID, _from_pos.x(), _from_pos.y(), cost))
                id += 1
                graph.D[_from][to] = graph.D[to][_from] = cost # doplnenie existujúcich hrán do matice vzdialeností
                
            # načítanie (optional) matice vzdialeností
            n = int(f.readline())
            for i in range(n):
                line = f.readline()
                dist = list(map(float, line.split()))
                graph.D[i] = dist
    #-------------------------------------------------------------------
    # uloží údaje do .txt súboru s rovnakým formátom, ako pri načítavaní
    #-------------------------------------------------------------------
    def save_data(self, network_path: str, save_dist, graph: VRP.Graph):
        with open(network_path, 'w') as f:
            # zápis vrcholov
            control_str = [len(graph.nodes), graph.capacity, graph.center] # prvý riadok pre vrcholy
            f.write(' '.join(map(str, control_str)) + '\n')
            for node in graph.nodes:
                node_str = [node.ID, round(node.pos().x(), 2), round(node.pos().y() * -1, 2), node.demand, node.name]
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