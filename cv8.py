import numpy as np
from math import floor
# vrcholy a ich pozície
nodes = [
    np.array([10, 10]),
    np.array([40, 20]),
    np.array([70, 20]),
    np.array([90, 20]),
    np.array([90, 50]),
    np.array([80, 80]),
    np.array([50, 60]),
    np.array([30, 40]),
    np.array([20, 80])
]
# matica vzdialeností - cez l2 normu z linalg.norm medzi 2 vrcholmi, najskôr sú inicializované iba susedné vrcholy z grafu, zaokrúhlené na celé čísla nadol
D = [
    [0, (floor((np.linalg.norm(nodes[1] - nodes[0])))), -1, -1, -1, -1, -1, (floor((np.linalg.norm(nodes[7] - nodes[0])))), -1],  # 1 susedná s 2 a 8
    [(floor((np.linalg.norm(nodes[1] - nodes[0])))), 0, (floor((np.linalg.norm(nodes[2] - nodes[1])))), -1, -1, -1, -1, (floor((np.linalg.norm(nodes[7] - nodes[1])))), -1], # 2 susedná s 1, 3, 8
    [-1, (floor((np.linalg.norm(nodes[2] - nodes[1])))), 0, (floor((np.linalg.norm(nodes[3] - nodes[2])))), (floor((np.linalg.norm(nodes[4] - nodes[2])))), -1, -1, -1, -1], # 3 susedná s 2, 4, 5
    [-1, -1, (floor((np.linalg.norm(nodes[3] - nodes[2])))), 0, -1, -1, -1, -1, -1], # 4 susedná s 3
    [-1, -1, (floor((np.linalg.norm(nodes[4] - nodes[2])))), -1, 0, -1, (floor((np.linalg.norm(nodes[6] - nodes[4])))), (floor((np.linalg.norm(nodes[7] - nodes[4])))), -1], # 5 susedná s 3, 7, 8
    [-1, -1, -1, -1, -1 , 0, (floor((np.linalg.norm(nodes[6] - nodes[5])))), -1, -1], # 6 susedná s 7
    [-1, -1, -1, -1, (floor((np.linalg.norm(nodes[4] - nodes[6])))), (floor((np.linalg.norm(nodes[5] - nodes[6])))), 0, (floor((np.linalg.norm(nodes[7] - nodes[6])))), (floor((np.linalg.norm(nodes[8] - nodes[6]))))], # 7 susedná s 5, 6, 8, 9
    [(floor((np.linalg.norm(nodes[0] - nodes[7])))), (floor((np.linalg.norm(nodes[1] - nodes[7])))), -1, -1, (floor((np.linalg.norm(nodes[4] - nodes[7])))), -1, (floor((np.linalg.norm(nodes[6] - nodes[7])))), 0, (floor((np.linalg.norm(nodes[8] - nodes[7]))))], # 8 susedná s 1, 2, 5, 7, 9
    [-1, -1, -1, -1, -1, -1, (floor((np.linalg.norm(nodes[6] - nodes[8])))), (floor((np.linalg.norm(nodes[7] - nodes[8])))), 0], # 9 susedná s 7, 8
]
# ostatné najkratšie cesty boli manuálne nájdené podľa matice D:
D[0][2] = D[0][1] + D[1][2] # cesta 1-3 = 1->2->3
D[0][3] = D[0][2] + D[2][3] # cesta 1-4 = 1->2->3->4
D[0][4] = D[0][7] + D[7][4] # cesta 1-5 = 1->8->5
D[0][5] = D[0][7] + D[7][6] + D[6][5] # cesta 1-6 = 1->8->7->6
D[0][6] = D[0][7] + D[7][6] # cesta 1-7 = 1->8->7
D[0][8] = D[0][7] + D[7][8] # cesta 1-9 = 1->8->9

D[1][3] = D[1][2] + D[2][3] # cesta 2-4 = 2->3->4
D[1][4] = D[1][2] + D[2][4] # cesta 2-5 = 2->3->5
D[1][5] = D[1][7] + D[7][6] + D[6][5] # cesta 2-6 = 2->8->7->6
D[1][6] = D[1][7] + D[7][6] # cesta 2-7 = 2->8->7
D[1][8] = D[1][7] + D[7][8] # cesta 2-9 = 2->8->9

D[2][0] = D[0][2] # cesta 3-1 # cesta 3-1 = 3->2->1
D[2][5] = D[2][4] + D[4][6] + D[6][5] # cesta 3-6 = 3->5->7->6
D[2][6] = D[2][4] + D[4][6] # cesta 3-7 = 3->5->7
D[2][7] = D[2][1] + D[1][7] # cesta 3-8 = 3->2->8
D[2][8] = D[2][7] + D[7][8] # cesta 3-9 = 3->2->8->9

D[3][0] = D[0][3] # cesta 4-1 = 4->3->2->1
D[3][1] = D[1][3] # cesta 4-2 = 4->3->2
D[3][4] = D[3][2] + D[2][4] # cesta 4-5 = 4->3->5
D[3][5] = D[3][2] + D[2][5] # cesta 4-6 = 4->3->5->7->6
D[3][6] = D[3][2] + D[2][6] # cesta 4-7 = 4->3->5->7
D[3][7] = D[3][2] + D[2][7] # cesta 4-8 = 4->3->2->8
D[3][8] = D[3][2] + D[2][8] # cesta 4-9 = 4->3->2->8->9

D[4][0] = D[0][4] # cesta 5-1 = 5->8->1 
D[4][1] = D[1][4] # cesta 5-2 = 5->3->2
D[4][3] = D[3][4] # cesta 5-4 = 5->3->4
D[4][5] = D[4][6] + D[6][5] # cesta 5-6 = 5->7->6
D[4][8] = D[4][6] + D[6][8] # cesta 5-9 = 5->7->9

D[5][0] = D[5][6] + D[0][6] # cesta 6-1 = 6->7->8->1
D[5][1] = D[5][6] + D[1][6] # cesta 6-2 = 6->7->8->2
D[5][2] = D[5][6] + D[2][6] # cesta 6-3 = 6->7->5->3
D[5][3] = D[5][6] + D[3][6] # cesta 6-4 = 6->7->5->3->4
D[5][4] = D[5][6] + D[6][4] # cesta 6-5 = 6->7->5
D[5][7] = D[5][6] + D[6][7] # cesta 6-8 = 6->7->8
D[5][8] = D[5][6] + D[6][8] # cesta 6-9 = 6->7->9

D[6][0] = D[0][6] # cesta 7-1 = 7->8->1
D[6][1] = D[1][6] # cesta 7-2 = 7->8->2
D[6][2] = D[2][6] # cesta 7-3 = 7->5->3
D[6][3] = D[3][6] # cesta 7-4 = 7->5->3->4

D[7][2] = D[2][7] # cesta 8-3 = 8->2->3
D[7][3] = D[3][7] # cesta 8-4 = 8->2->3->4
D[7][5] = D[5][7] # cesta 8-6 = 8->7->6

D[8][0] = D[0][8] # cesta 9-1 = 9->8->1
D[8][1] = D[1][8] # cesta 9-2 = 9->8->2
D[8][2] = D[2][8] # cesta 9-3 = 9->8->2->3
D[8][3] = D[3][8] # cesta 9-4 = 9->8->2->3->4
D[8][4] = D[4][8] # cesta 9-5 = 9->7->5
D[8][5] = D[5][8] # cesta 9-6 = 9->7->6
# vektor požiadaviek a kapacita vozidla, počet vrcholov
b = [100, 300, 400, 200, 100, 200, 500, 300, 100]
capacity = 700
no_nodes = len(nodes)

#-------------------------------------------------------------------------------------------------------------------------------
# vráti riešenie TSP pomocou metódy najbližšieho suseda zo zadaného indexu, index v parametre je číslo vrchola, teda začína od 1 
#-------------------------------------------------------------------------------------------------------------------------------
def get_route_NN(start_node):
    nodes_in_route = [0] * no_nodes  # vektor značiek pre prejdené vrcholy
    route = []
    nodes_in_route[start_node - 1] = 1
    route.append(start_node - 1)
    route_length = 0
    
    for i in range(no_nodes - 1):
        nearest_neighbor = 0
        nearest_length = 5000000
        current_node = route[-1]  # posledný prvok v ceste - hľadáme jeho najbližšieho suseda
        
        for j in range(no_nodes):
            if (D[current_node][j] < nearest_length and nodes_in_route[j] == 0):
                nearest_neighbor = j
                nearest_length = D[current_node][j]
                
        route.append(nearest_neighbor)
        nodes_in_route[nearest_neighbor] = 1
        route_length += D[current_node][nearest_neighbor]
    
    route.append(start_node - 1)  # nakoniec sa pridá počiatočný vrchol na uzavretie trasy
    
    return route, route_length
#-------------------------------------------------------------------------------------------------------------------------------------------------
# rozdelí trasu získanú v "get_route_NN" ako výsledok TSP na jednotlivé jazdy/zhluky, ktoré následne vráti aj s využitou kapacitou pre každú jazdu
#-------------------------------------------------------------------------------------------------------------------------------------------------
def get_subtoures(route):
    routes = []
    used_capacity = 0
    subtour = []
    subtour.append(route[0])
    
    for i in range(1, len(route) - 1):
        subtour.append(route[i])
        used_capacity += b[route[i]]
        next_node = route[i + 1]
        
        if i == (len(route) - 2) or (b[next_node] + used_capacity) > capacity:
            subtour.append(route[0])
            routes.append((subtour, used_capacity))
            subtour = []
            subtour.append(route[0])
            used_capacity = 0
            
    
    return routes
    
#------------------------------------------------------------------------------------------------------------------------
# pomocná metóda, ktorá zoberie subtoures tuple (list vrcholov, využitá kapacita) a spraví z každej jazdy string na print
#------------------------------------------------------------------------------------------------------------------------
def get_subtoures_strings(subtoures):
        strings = []
        for i in range(len(subtoures)):
            string = ""
            subtour_tuple = subtoures[i]
            
            for j in range(len(subtour_tuple[0]) - 1):
                string += f"{subtour_tuple[0][j] + 1}->"
            string += f"{subtour_tuple[0][0] + 1}\nUsed capacity: {subtour_tuple[1]}"
            strings.append(string)
            
        return strings
    
def main():
    TSP_route, TSP_length = get_route_NN(3)
    TSP_route_print = ""
    
    for i in range(len(TSP_route) - 1):
        TSP_route_print += f"{TSP_route[i] + 1}->"
    TSP_route_print += f"{TSP_route[-1] + 1}"
        
    subtoures = get_subtoures(TSP_route)
    subtoures_print = get_subtoures_strings(subtoures)
    
    print("/////////////////////////////////////////////////////////////////////")
    print("Vehicle Routing Problem")
    print(f"Number of nodes: {no_nodes}")
    print("Method used: Route First-Cluster Second")
    print("---------------------------------------------------------------------")
    print(f"TSP route using nearest neighbor: {TSP_route_print}")
    print(f"TSP route length: {TSP_length}")
    print("---------------------------------------------------------------------")
    print("Subtoures (clusters):")
    for i in range(len(subtoures)):
        print(f"Subtour {i+1}:")
        print(f"{subtoures_print[i]}\n")
    print("/////////////////////////////////////////////////////////////////////")
    
    
main()