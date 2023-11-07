import random
from time import gmtime, strftime, localtime
from PIL import Image, ImageDraw

'''Maze generator in PNG with various algorithm'''


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

        creation_algorithms[algo](self) #Apply the function based on the name in the dict
 
    def select_cell_by_coord(self, coord):
        for cell in self.cells:
            if coord == cell.coord:
                return cell

    def random_cell(self):
        random_cell = random.choice(self.Cells)
        return random_cell
                
    def create_png(self):
        return draw_PNG(self)
        
    
def draw_PNG(Grid, cell_size:int = 20, bg_color = (255,255,255), wall_color = (0,0,0), distance:bool = False):  
    """
    Using the PIL module and on an object of class Grid, 
    this function allows to draw the maze in PNG. 
    The grid is made of black squares for each cell 
    and the walls are painted white when two cells are connected 
    to visually open the passage
    """
    
    image_width = cell_size * Grid.col
    image_height = cell_size * Grid.lines
    border = 20

    image = Image.new("RGBA", (image_width + border, image_height + border), (255,255,255))
    draw = ImageDraw.Draw(image)

    for i in range(2):
        for cell in Grid.cells:
            x1 = 10 + cell.x * cell_size
            y1 = 10 + cell.y * cell_size
            x2 = 10 + (cell.x + 1) * cell_size
            y2 = 10 + (cell.y + 1) * cell_size

            if i == 0: #First pass to draw a wall rectangle for each cell
                draw.rectangle([(x1, y1), (x2, y2)], outline=wall_color, fill = bg_color, width=1)
                draw.text(((x1 + x2)/2,(y1 + y2)/2), cell.content, fill = wall_color, anchor = "ms")
            else: #Second pass (because range = 0 or 1) to replace black wall by white when open
                if cell.north_cell is not None and cell.north_cell.coord in cell.links:
                    draw.line([(x1+1,y1),(x2-1,y1)], fill=bg_color, width=1)
                if cell.south_cell is not None and cell.south_cell.coord in cell.links:
                    draw.line([(x1+1,y2),(x2-1,y2)], fill=bg_color, width=1)
                if cell.east_cell is not None and cell.east_cell.coord in cell.links:                        
                    draw.line([(x2,y1+1),(x2,y2-1)], fill=bg_color, width=1)
                if cell.west_cell is not None and cell.west_cell.coord in cell.links:        
                    draw.line([(x1,y1+1),(x1,y2-1)], fill=bg_color, width=1)
    
        
            

    #filename = strftime("%Y_%m_%d_%H_%M_%S", localtime())
    #image.save("{}.png".format(filename), "PNG", optimize=True)
    return image


def binary_tree(Grid):
    """ 
    Fast, efficient, and simple
    Strongly biased toward diagonals (here NE)
    """
    for cell in Grid.cells:
        neighbors = []
        if cell.north_cell is not None:
            neighbors.append(cell.north_cell)
        if cell.east_cell is not None:
            neighbors.append(cell.east_cell)
        if neighbors:
            neighbor = random.choice(neighbors)
            if neighbor:
                cell.dig(neighbor)


def aldous_broder(Grid):
    """
    Perfect randomly maze
    Long to finish in big mazes ++
    """
    actual_cell = random.choice(Grid.cells)
    not_yet_visited = len(Grid.cells)-1

    while not_yet_visited > 0:
        neighbors = actual_cell.neighbors
        neighbor = random.choice(neighbors)
        if not neighbor.links: #If list is not empty (empty = False)
            actual_cell.dig(neighbor)
            not_yet_visited -= 1
        actual_cell = neighbor

def hunt_and_kill(Grid):
    """
    Few dead-ends, long rivers
    Low memory, but slow
    """
    actual_cell = random.choice(Grid.cells)

    while actual_cell is not None:
        not_visited_neighbors = [neighbor for neighbor in actual_cell.neighbors if len(neighbor.links) == 0]
        if not_visited_neighbors:
            neighbor = random.choice(not_visited_neighbors)
            actual_cell.dig(neighbor)
            actual_cell = neighbor
        else:
            actual_cell = None
            for i in Grid.cells:
                visited_neighbors = [neighbor for neighbor in i.neighbors if len(neighbor.links) > 0]
                if not i.links and visited_neighbors:
                   actual_cell = i
                   neighbor = random.choice(visited_neighbors)
                   actual_cell.dig(neighbor)
                   break 



# Dict containing the list of algorithms 
creation_algorithms = {
    "bt":binary_tree, 
    "ab":aldous_broder, 
    "hk":hunt_and_kill,
    }
        

        
        
if __name__ == "__main__":
    #Tests processing
    
    test = Grid(algo="ab")
    test.create_png()
  
