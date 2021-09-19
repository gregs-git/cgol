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
    """create a matrix of random ones and zeros"""
    grid = np.random.randint(2, size=(rows, columns))
    return grid

def add_zero_border(grid):
    """add a border of zeros""" 
    grid = np.pad(grid,1)
    return grid

def get_grid_state(grid):
    """get the state of the grid"""
    grid_state = ''.join([str(x) for x in list(chain.from_iterable(grid))])
    return grid_state

def get_cell(grid, row, column):
    cell = grid[row, column]
    return cell

def get_living_neighbours(grid, row, column):
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
    next_grid=[]
    for row in range(1, rows+1):
        for column in range(1, columns+1):
            cell = get_cell(grid, row, column)
            living_neighbours = get_living_neighbours(grid, row, column)
            new_cell_value = rules_of_life(cell, living_neighbours)
            next_grid.append(new_cell_value)
    next_grid = np.array(next_grid).reshape(rows,columns)
    next_grid = add_zero_border(next_grid)
    return next_grid

def process_grid(grid, rows, columns):
    next_grid = get_next_grid(grid, rows, columns)
    grid = next_grid
    return grid

def get_full_turn_set(grid, turns_db, turns):
    while True:    
        grid = process_grid(grid, rows, columns)
        grid_state = get_grid_state(grid)
        if grid_state in turns_db:
            print("Complete")
            break
        else:
            turns_db.append(grid_state)
            turns += 1
            print(grid)
            print(turns)

def process_all_seeds(rows, columns):
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
print(2**(rows*columns))
