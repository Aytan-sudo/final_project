from PIL import Image, ImageDraw
from time import localtime, strftime

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
    
        
            

    filename = strftime("%Y_%m_%d_%H_%M_%S", localtime())
    image.save("{}.png".format(filename), "PNG", optimize=True)


