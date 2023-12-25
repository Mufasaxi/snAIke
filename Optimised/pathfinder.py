class Pathfinder:
    def __init__(self, rows: int, cols: int) -> None:
        self.cols = cols
        self.rows = rows

    def makeGrid(self, rows: int, cols: int) -> list[list[int]]:
        return [[0 for col in range(cols)] for row in range(rows)]

    def numberCells(self, grid: list[int]) -> list[list[int]]:
        total = len(grid) * len(grid[0])
        count = 0
        outputGrid = self.makeGrid(len(grid), len(grid[0]))
        while count < total:
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    outputGrid[row][col] = count
                    count += 1
        return outputGrid

    def findIndex(self, nestedList: list[list[int]], element: int) -> list[list[int]]:
        return [[i, el.index(element)] for i, el in enumerate(nestedList) if element in el]

    def calculateEdgeCosts(self, adjacencyList: dict[int, list[int]], grid: list[list[int]], numGrid: list[list[int]]) -> dict[tuple[int], int]:
        edgeCosts = {}

        for node in adjacencyList:
            for neighbour in adjacencyList[node]:
                neighbourIndex = self.findIndex(numGrid, neighbour)
                neighbourY = neighbourIndex[0][0]
                neighbourX = neighbourIndex[0][1]

                edgeCosts[node, neighbour] = grid[neighbourY][neighbourX]
        
        return edgeCosts

    def makeAdjacencyList(self, grid: list[list[int]]) -> list[list[int]]:
        lst = {grid[row][col]: [] for row in range(len(grid)) for col in range(len(grid[0]))}

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                neighbours = self.calculateNeighbours(grid, row, col)
                lst[grid[row][col]] = neighbours

        return lst

    def calculateNeighbours(self, grid: list[list[int]], row: int, col: int) -> list[int]:
        potentialNeighbours = [(col-1, row), (col+1, row), (col, row-1), (col, row+1)]
        neighbourIndices = []

        for i, neighbour in enumerate(potentialNeighbours):
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(grid[0]) or neighbour[1] >= len(grid):
                potentialNeighbours[i] = None
        neighbourIndices =  [neighbour for neighbour in potentialNeighbours if neighbour is not None]

        neighbours = [grid[index[1]][index[0]] for index in neighbourIndices]
        return neighbours


    def printGrid(self, grid: list[list[int]]):
        for row in grid:
            print(row)

    def getCoord(self, point: int) -> list[int]:
        x = point % self.cols # value mod cols
        y = point // self.cols # value // cols
        return [x, y]

    # A star heuristic using Manhattan distance (Taxicab distance)
    def taxiCabDist(self, points: list[list[int]], destination: int) -> dict[int, int]:
        h = dict()
        for row in points:
            for point in row:
                pointX, pointY = self.getCoord(point)[0], self.getCoord(point)[1]
                destX, destY = self.getCoord(destination)[0], self.getCoord(destination)[1]
                h[point] = abs(pointX - destX) + abs(pointY - destY) # abs(X1 - X2) + (Y1 - Y2)
        return h


    def a_star(self, G: dict[int, list[int]], cost: dict[tuple[int], int], taxiCabDist: dict[int, int], origin: int, destination: int) -> list[int]:
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

        return path #, l[destination], visited