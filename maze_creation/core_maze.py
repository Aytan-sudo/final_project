import random
import algo_maze
import print_maze
from time import gmtime, strftime

'''Only the generation of maze in png work at that time'''


class Cell: #A maze is made up of cells

    def __init__(self, x:int, y:int):
        self.coord = (x,y)
        self.x = x
        self.y = y
        self.links = []
        self.north_cell = None
        self.south_cell = None
        self.east_cell = None
        self.west_cell = None
        self.neighbors = []
        self.content = " "

    #def __repr__(self):
        #return str(self.coord)

    def dig(self, cell): #Link two Cells
        self.links.append(cell.coord)
        cell.links.append(self.coord)

    def neighbors_create(self): #Define list of neighbours for use in some algorithms
        if self.north_cell is not None:
            self.neighbors.append(self.north_cell)
        if self.south_cell is not None:
            self.neighbors.append(self.south_cell)
        if self.east_cell is not None:
            self.neighbors.append(self.east_cell)
        if self.west_cell is not None:
            self.neighbors.append(self.west_cell)
     
    def distances(self): #Not yet validated
        distances = Distances(self)
        frontier = [self]

        while frontier:
            new_frontier = []

            for cell in frontier:
                for linked in cell.links:
                    if distances[linked]:
                        continue
                    distances[linked] = distances[cell] + 1
                    new_frontier.append(linked)

            frontier = new_frontier

        return distances
        

class Grid:
    def __init__(self, col:int = 20, lines:int = 20, algo:str = "ab"):
        self.col = col
        self.lines = lines
        self.algo = algo
        self.cells = []

        for i in range(self.col): #create grid.cells (list of cells)
            for ii in range(self.lines):
                self.cells.append(Cell(i,ii))

        for i in self.cells: #define coordinates of neighborgs cells only if in the grid
            if 0 < i.y < self.lines:
                for ii in self.cells:
                    if ii.coord == (i.x,i.y-1):
                        i.north_cell = ii
            if 0 < i.y+1 < self.lines:
                for ii in self.cells:
                    if ii.coord == (i.x,i.y+1):
                        i.south_cell = ii
            if 0 < i.x < self.col:
                for ii in self.cells:
                    if ii.coord == (i.x-1,i.y):
                        i.west_cell = ii
            if 0 < i.x+1 < self.col:
                for ii in self.cells:
                    if ii.coord == (i.x+1,i.y):
                        i.east_cell = ii
            i.neighbors_create()

        algo_maze.creation_algorithms[algo](self) #Apply the function based on the name in the dict
 
    def select_cell_by_coord(self, coord):
        for cell in self.cells:
            if coord == cell.coord:
                return cell

    def random_cell(self):
        random_cell = choice(self.Cells)
        return random_cell
                
    def create_png(self):
        print_maze.draw_PNG(self)
        
class Distances: #not yet validated
    def __init__(self, root:Cell):
        self._root = root
        self._cells = dict()
        self._cells[root] = 0

    def __getitem__(self, cell:Cell):
        if cell in self._cells.keys():
            return self._cells[cell]
        return None

    def __setitem__(self, cell:Cell, distance:int):
        self._cells[cell] = distance

    def cells(self):
        return list(self._cells.keys())

    def path_to(self, goal):
        current = goal

        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self.cells[current]

        while current != self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break
        return breadcrumbs

        
        
if __name__ == "__main__":
    #Tests processing
    
    test = Grid(algo="ab")
    test.create_png()
  
