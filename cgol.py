import numpy as np
from itertools import chain
from time import sleep

rows = 3
columns = 3
starting_state_db = []
starting_grid_state = str()
turns_db = []
next_grid = []
turns = 0

def create_grid(rows, columns):
    """Create a grid from a matrix of randomly generated ones and zeros."""
    grid = np.random.randint(2, size=(rows, columns))
    return grid

def add_zero_border(grid):
    """Add a border of zeros as extra cells to a grid.""" 
    grid = np.pad(grid,1)
    return grid

def get_grid_state(grid):
    """Convert a whole grid to a string of ones and zeros."""
    grid_state = ''.join([str(x) for x in list(chain.from_iterable(grid))])
    return grid_state

def get_cell(grid, row, column):
    """Select a cell in the grid by its co-ordinate."""
    cell = grid[row, column]
    return cell

def get_living_neighbours(grid, row, column):
    """Calculate the sum of all cell values surrounding a given cell
    to return the total number of living neighbours."""
    neighbours = (
    get_cell(grid, row-1, column-1)
    ,get_cell(grid, row-1, column)
    ,get_cell(grid, row-1, column+1)
    ,get_cell(grid, row, column-1)
    ,get_cell(grid, row, column+1)
    ,get_cell(grid, row+1, column-1)
    ,get_cell(grid, row+1, column)
    ,get_cell(grid, row+1, column+1))
    living_neighbours = sum(neighbours)
    return living_neighbours

def rules_of_life(cell, living_neighbours):
    """Apply the Rules to a given cell using the sum of its neighbours
    and return a new value for that cell of one or zero accordingly."""
    if cell == 1:
        if living_neighbours == 0 or living_neighbours == 1:
            return 0
        elif living_neighbours == 2 or living_neighbours == 3:
            return 1
        elif living_neighbours > 3:
            return 0
    elif cell == 0:
        if living_neighbours == 3:
            return 1
        else:
            return 0

def get_next_grid(grid, rows, columns):
    """Apply the rules to each cell in a grid, excluding the border of zeros,
    and return a new grid from the result, with a border added."""
    next_grid=[]
    for row in range(1, rows+1):
        for column in range(1, columns+1):
            cell = get_cell(grid, row, column)
            living_neighbours = get_living_neighbours(grid, row, column)
            new_cell_value = rules_of_life(cell, living_neighbours)
            next_grid.append(new_cell_value)
    next_grid = np.array(next_grid).reshape(rows,columns)
    next_grid = add_zero_border(next_grid)
    return grid

def get_full_turn_set(grid, turns_db, turns):
    """Create new grids from an initial grid by applying the rules 
    successively until a grid that has already been seen is created"""
    while True:    
        grid = get_next_grid(grid, rows, columns)
        grid_state = get_grid_state(grid)
        if grid_state in turns_db:
            break
        else:
            turns_db.append(grid_state)
            turns += 1
            print(grid)
            print(turns)

def process_all_seeds(rows, columns):
    """Generate and process every possible initial grid combination
    and return number total initial grids processed"""
    starting_state_db = []
    while len((starting_state_db)) < 2**(rows*columns):   
        grid = create_grid(rows, columns)
        grid = add_zero_border(create_grid(rows, columns))
        starting_grid_state = get_grid_state(grid)
        if starting_grid_state in starting_state_db:
            print(len(starting_state_db), 2**(rows*columns))
        else:
            starting_state_db.append(starting_grid_state)
            turns_db = []
            get_full_turn_set(grid, turns_db, turns)
    return len(starting_state_db)

process_all_seeds(rows, columns)
