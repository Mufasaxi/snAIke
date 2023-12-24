def makeGrid(rows , cols):
    return [[0 for col in range(cols)] for row in range(rows)]

def numberCells(grid):
    total = len(grid) * len(grid[0])
    count = 0
    outputGrid = makeGrid(len(grid), len(grid[0]))
    while count < total:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                outputGrid[row][col] = count
                count += 1
    return outputGrid

def findIndex(nestedList, element):
    return [(i, el.index(element)) for i, el in enumerate(nestedList) if element in el]

def calculateEdgeCosts(adjacencyList, grid, numGrid):
    edgeCosts = {}

    for node in adjacencyList:
        for neighbour in adjacencyList[node]:
            neighbourIndex = findIndex(numGrid, neighbour)
            neighbourY = neighbourIndex[0][0]
            neighbourX = neighbourIndex[0][1]

            edgeCosts[node, neighbour] = grid[neighbourY][neighbourX]
    
    return edgeCosts

def makeAdjacencyList(grid):
    lst = {grid[row][col]: [] for row in range(len(grid)) for col in range(len(grid[0]))}

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            neighbours = calculateNeighbours(grid, row, col)
            lst[grid[row][col]] = neighbours

    return lst

def calculateNeighbours(grid, row, col):
    potentialNeighbours = [(col-1, row), (col+1, row), (col, row-1), (col, row+1)]
    neighbourIndices = []

    for i, neighbour in enumerate(potentialNeighbours):
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(grid[0]) or neighbour[1] >= len(grid):
            potentialNeighbours[i] = None
    neighbourIndices =  [neighbour for neighbour in potentialNeighbours if neighbour is not None]

    neighbours = [grid[index[1]][index[0]] for index in neighbourIndices]
    return neighbours


def printGrid(grid):
    for row in grid:
        print(row)


# grid = makeGrid(5,10)
# numberedGrid = numberCells(grid)
# adjList = makeAdjacencyList(numberedGrid)
# costs = calculateEdgeCosts(adjList, grid, numberedGrid)
# print('GRID:')
# printGrid(grid)
# print('NUMBERED GRID:')
# printGrid(numberedGrid)
# print('ADJACENCY LIST:')
# print(adjList)
# print('COSTS:')
# print(costs)

testGrid = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

numberedGrid = numberCells(testGrid)
adjList = makeAdjacencyList(numberedGrid)
costs = calculateEdgeCosts(adjList, testGrid, numberedGrid)
# print('GRID:')
# printGrid(testGrid)
# print('NUMBERED GRID:')
# printGrid(numberedGrid)
# print('ADJACENCY LIST:')
# print(adjList)
# print('COSTS:')
# print(costs)

def getCoord(point):
    x = point % 20 # value mod cols
    y = point // 20 # value // cols
    return [x, y]

# A star heuristic using Manhattan distance (Taxicab distance)
def taxiCabDist(points, destination):
    h = dict()
    for row in points:
        for point in row:
            pointX, pointY = getCoord(point)[0], getCoord(point)[1]
            destX, destY = getCoord(destination)[0], getCoord(destination)[1]
            h[point] = abs(pointX - destX) + abs(pointY - destY) # abs(X1 - X2) + (Y1 - Y2)
    return h


def a_star(G, cost, taxiCabDist, origin, destination):
    l = {destination: float("inf")}
    pred = dict()
    path = list()
    visited = set()
    closed = set()
    f = 0
    nodes = dict()

    def f_cost(node):
        f = l[node] + taxiCabDist[node]
        return f

    for v in G:
        l[v] = float("inf")

    l[origin] = 0
    visited.add(origin)

    while len(visited) != 0:
        for node in visited:
            nodes[node] = f_cost(node)
        v = min(nodes, key=nodes.get)
        nodes.pop(v)
        visited.discard(v)
        closed.add(v)
        if v == destination:
            if destination in pred:
                path = [destination]
                while path[0] != origin:
                    path.insert(0, pred[path[0]])
            return path, l[destination], visited
        else:
            for w in G[v]:
                if w not in visited and w not in closed:
                    visited.add(w)
                    l[w] = l[v] + cost[v,w]
                    pred[w] = v
                else:
                    if l[w] > l[v] + cost[v,w]:
                        l[w] = l[v] + cost[v,w]
                        pred[w] = v
                        if w in closed:
                            closed.discard(w)
                            visited.add(w)


    if destination in pred:
        path = [destination]
        while path[0] != origin:
            path.insert(0, pred[path[0]])

    return path, l[destination], visited



# Testing with Dijkstra
def dijkstra(G, c, maxDist, origin, destination):
    l = {}
    pred = {}
    path = []
    R = []
    visited = {}  # dies brauchen wir damit die schon besuchten Knoten nicht zweimal geprueft werden

    # Initialisierung von Dijkstra
    # Origin wird auf 0 gesetzt und alle anderen auf unendlich
    for v in G:
        l[v] = 10000000000000  # sys.maxint konnte stattdesssen genutzt werden wenn die importierung von Bibliotheken erlaubt

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
    print('p',pred)
    if destination in pred:
        path = [destination]
        while path[0] != origin:
            path.insert(0, pred[path[0]])

    return path


maxDist = 600000  # maximale Fahrdistanz zwischen zwei Knoten in Metern

G, c = adjList, costs#read_graph('Optimised/graph.txt')
origin = numberedGrid[6][11]  # Startknoten
destination = numberedGrid[9][5]  # Endknoten

path = dijkstra(G, c, maxDist, origin, destination)
print('t')
printGrid(testGrid)
print('n')
printGrid(numberedGrid)
print("DIJKSTRA Kürzester Weg:", path) # since many ways have the shortest path cost wise we need to find the shortest path node wise too, this doesnt do it

taxiDists = taxiCabDist(numberedGrid, destination)
path2 = a_star(G, c, taxiDists, origin, destination)
print("A STAR path:", path2[0])