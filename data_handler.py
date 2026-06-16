from pathlib import Path
import VRP_graph as VRP
import node
import edge

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
                _type = 0 if id != graph.center else 1
                graph.nodes.append(node.Node(id, x, y, demand, name, _type))
            
            # načítanie hrán
            n, graph.mode_edges = map(int, f.readline().split())
            for i in range(n):
                _from = to = cost = -1
                if graph.mode_edges == 0:
                    _from, to, cost = f.readline().split()
                elif graph.mode_edges == 1:
                    _from, to = f.readline().split()
                    
                graph.edges.append(edge.Edge(i, _from, to, cost)) 
                
            # načítanie (optional) matice vzdialeností
            n = int(f.readline())
            for i in range(n):
                line = f.readline()
                dist = list(map(int, line.split()))
                graph.D.append(dist)
    #-------------------------------------------------------------------
    # uloží údaje do .txt súboru s rovnakým formátom, ako pri načítavaní
    #-------------------------------------------------------------------
    def save_data(self, network_path: str, save_dist, graph: VRP.Graph):
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