from py_objects import Gridcell, Grid

def generate_grid(gridsize: tuple[int, int]) -> Grid:
    grid = Grid(gridsize)
    return grid