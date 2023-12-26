class Pathfinder:
    def __init__(self, rows: int, cols: int) -> None:
        self.cols = cols
        self.rows = rows

    def make_grid(self, rows: int, cols: int) -> list[list[int]]:
        '''
        Returns a grid of width 'rows' and height 'cols' with 0 in all entries.

        Parameters:
            rows: number of rows.
            cols: number of columns.

        Returns:
            grid: Grid of width 'rows' and height 'cols' with 0 in all entries.
        '''
        return [[0 for col in range(cols)] for row in range(rows)]

    def number_cells(self, grid: list[list[int]]) -> list[list[int]]:
        '''
        Returns a numbered grid with 0 at the top left corner, and the last element in the bottom right corner.

        Parameters:
            grid: Grid with cells that need numbering

        Returns:
            numbered_grid: Grid with cells that are numbered from the top left corner to the bottom right corner.
        '''
        total = len(grid) * len(grid[0])
        count = 0
        numbered_Grid = self.make_grid(len(grid), len(grid[0]))
        while count < total:
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    numbered_Grid[row][col] = count
                    count += 1
        return numbered_Grid

    def find_index(self, nestedList: list[list[int]], element: int) -> list[list[int]]:
        '''
        Returns the index of a given element that's in a nested list.

        Parameters:
            nested_list: Nested list containing the element to look for.

        Returns:
            [i, j]: List containing the indices of the element in the nested list.
        '''
        return [[i, el.index(element)] for i, el in enumerate(nestedList) if element in el]

    def calculate_edge_costs(self, adjacencyList: dict[int, list[int]], grid: list[list[int]], numGrid: list[list[int]]) -> dict[tuple[int], int]:
        '''
        Returns the edge costs of cells in a grid

        Parameters:
            adjacency_list: Adjacency list containing all cells as keys and their respective neighbours as values.
            grid: Grid containing the cells.
            num_grid: Grid with numbered cells.

        Returns:
            edge_costs: Dictionary containing neighbours as keys and the cost of the edge connecting them as value.
        '''
        edge_costs = {}

        for node in adjacencyList:
            for neighbour in adjacencyList[node]:
                neighbour_index = self.find_index(numGrid, neighbour)
                neighbourY = neighbour_index[0][0]
                neighbourX = neighbour_index[0][1]

                edge_costs[node, neighbour] = grid[neighbourY][neighbourX]
        
        return edge_costs

    def make_adjacency_list(self, grid: list[list[int]]) -> list[list[int]]:
        '''
        Creates an adjacency list of a given graph / grid.

        Parameters:
            grid: Grid / graph that contains the cells
        
        Returns:
            lst: Adjacency list (as a dictionary) containing each cell as a key and a list of neighbours as value.
        '''
        lst = {grid[row][col]: [] for row in range(len(grid)) for col in range(len(grid[0]))}

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                neighbours = self.calculate_neighbours(grid, row, col)
                lst[grid[row][col]] = neighbours

        return lst

    def calculate_neighbours(self, grid: list[list[int]], row: int, col: int) -> list[int]:
        '''
        Calculates neighbouring cells for all cells in a grid.

        Parameters:
            grid: Grid containing all cells.
            row: Row of cell, whose neighbours we want to know.
            col: Columsn of cell, whose neighbours we want to know.

        Returns:
            neighbours: List containing all neighbours. 
        '''
        potential_neighbours = [(col-1, row), (col+1, row), (col, row-1), (col, row+1)]
        neighbour_indices = []

        for i, neighbour in enumerate(potential_neighbours):
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(grid[0]) or neighbour[1] >= len(grid):
                potential_neighbours[i] = None
        neighbour_indices =  [neighbour for neighbour in potential_neighbours if neighbour is not None]

        neighbours = [grid[index[1]][index[0]] for index in neighbour_indices]
        return neighbours


    def print_grid(self, grid: list[list[int]]):
        '''
        Outputs a given grid line by line

        Parameters:
            grid: Grid (as nested list) that needs to be outputted.

        Returns
            None, this only outputs a grid line by line on the console

        '''
        for row in grid:
            print(row)

    def get_coords(self, point: int) -> list[int]:
        '''
        Returns the x (row) and y (column) coordinate of a given point from a numbered grid.

        Parameters:
            point: Numbered cell, whose x and y coordinate needs to be calculated.
        
        Returns:
            list: List containing x and y values of given numbered cell (point).
        '''
        x = point % self.cols # value mod cols
        y = point // self.cols # value // cols
        return [x, y]

    # A star heuristic using Manhattan distance (Taxicab distance)
    def taxi_cab_distance(self, points: list[list[int]], destination: int) -> dict[int, int]:
        '''
        Heuristic used for calculating the F function for the A* algorithm. Calculates Manhattan / Taxi cab distance. (abs(X1 - X2) + abs(Y1 - Y2))

        Parameters:
            points: List of numbered cells in a grid.
            destination: Numbered cell, that is the destination of the A* algorithm.

        Returns:
            h: Dictionary containing taxi cab distance from all cells to the destination cell.
        '''
        h = dict()
        for row in points:
            for point in row:
                pointX, pointY = self.get_coords(point)[0], self.get_coords(point)[1]
                destX, destY = self.get_coords(destination)[0], self.get_coords(destination)[1]
                h[point] = abs(pointX - destX) + abs(pointY - destY)
        return h


    def a_star(self, G: dict[int, list[int]], cost: dict[tuple[int], int], taxi_cab_distance: dict[int, int], origin: int, destination: int) -> list[int]:
        '''
        Applies the A* algorithm on given Graph / grid to find shortest path from origin to destination.

        Parameters:
            G: Graph / Grid (as adjacency list) where the algorithm needs to be applied.
            cost: Dictionary containing the costs of edges between each cell and its neighbours.
            taxi_cab_distance: Dictionary containing the Taxi cab distance from each cell to the destination cell.
            origin: Number of origin cell in a numbered grid.
            destination: Number of destination cell in a numbered grid.
        
        Returns:
            path: List containing the shortest path from origin to destination
        '''
        l = {destination: float("inf")}
        pred = dict()
        path = list()
        visited = set()
        closed = set()
        f = 0
        nodes = dict()

        def f_cost(node):
            f = l[node] + taxi_cab_distance[node]
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