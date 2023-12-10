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


grid = makeGrid(5,10)
numberedGrid = numberCells(grid)
adjList = makeAdjacencyList(numberedGrid)
print('GRID:')
printGrid(grid)
print('NUMBERED GRID:')
printGrid(numberedGrid)
print('ADJACENCY LIST:')
print(adjList)