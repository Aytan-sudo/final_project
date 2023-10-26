import random



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
        
