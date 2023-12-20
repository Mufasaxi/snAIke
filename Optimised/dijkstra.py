"""
Liest einen Graphen in der Form einer Liste (E Startknoten Endknoten Kantengewicht) ein
"""


def read_graph(filepath):
    G = {}
    c = {}
    # Zeilenweise Einlesen der graph.txt
    f = open(filepath, 'r')
    lines = f.read().splitlines()
    for l in lines:
        s = l.split(' ')
        if s[0] == 'E':
            if s[1] not in G.keys():
                G[s[1]] = []
            if s[2] not in G.keys():
                G[s[2]] = []
            G[s[1]].append(s[2])
            c[s[1], s[2]] = int(s[3])
            c[s[2], s[1]] = int(s[3])
    # Erzeugt einen ungerichteten Graphen
    for v1 in G:
        for v2 in G[v1]:
            if v1 not in G[v2]:
                G[v2].append(v1)
    print(G)
    print('----------------')
    print(c)
    print('----------------')
    return G, c


"""
Implementierung des Dijkstra-Algorithmus

	G = Graph als Adjazenzliste
	c = Distanzen zwischen den Knoten; koennen mit c[v1,v2] abgefragt werden
	origin = Startknoten
	destination = Endknoten
	maxDist = maximale Fahrdistanz zwischen zwei Knoten

	path = [origin, ..., destination] - kuerzester Weg zwischen origin und destination
"""


def dijkstra(G, c, maxDist, origin, destination):
    l = {}
    pred = {}
    path = []
    R = []
    visited = {}  # dies brauchen wir damit die schon besuchten Knoten nicht zweimal geprueft werden

    # Initialisierung von Dijkstra
    # Origin wird auf 0 gesetzt und alle anderen auf unendlich
    for v in G:
        l[
            v] = 10000000000000  # sys.maxint konnte stattdesssen genutzt werden wenn die importierung von Bibliotheken erlaubt

    l[origin] = 0

    for v in G:
        visited[v] = False

    nodes = list(G.keys())
    while len(nodes) != len(R):
        v = min(l, key=l.get)  # um auf den Knoten mit der niedrigsten Laenge zu greifen
        while visited[v] is False:
            R.append(v)
            for w in G[v]:
                if w not in R:
                    if c[v, w] <= maxDist:
                        if l[w] > l[v] + c[v, w]:
                            l[w] = l[v] + c[v, w]
                            pred[w] = v
            visited[v] = True
            l[v] = 10000000000000 # damit diese v mit den niedrigsten Wert nicht immer aufgewahelt wird

    if destination in pred:
        path = [destination]
        while path[0] != origin:
            path.insert(0, pred[path[0]])

    return path


"""
	Testszenario startet hier
	ACHTUNG: Bei zu kleinem maxDist koennte es keine Loesung mehr geben
"""
maxDist = 600000  # maximale Fahrdistanz zwischen zwei Knoten in Metern

G, c = read_graph('Optimised/graph.txt')
origin = "Lissabon"  # Startknoten
destination = "Stockholm"  # Endknoten

path = dijkstra(G, c, maxDist, origin, destination)

print("Kürzester Weg:", path)
