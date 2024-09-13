from py_objects import Gridcell, Grid
from random import choice

def generate_grid(gridsize: tuple[int, int]) -> Grid:
    grid = Grid(gridsize)
    return grid

def shift_origin(grid: Grid) -> None:
    # Figure out valid direction by whether the origin is at thee edge of the grid.
    valid_directions: list[str] = []
    if not (grid.origin[0] == grid.gridsize[0]-1): valid_directions.append("Right")
    if not (grid.origin[1] == grid.gridsize[1]-1): valid_directions.append("Bottom")
    if not (grid.origin[0] == 0): valid_directions.append("Left")
    if not (grid.origin[1] == 0): valid_directions.append("Top")
    # Pick a valid direction.
    shift_direction: str = choice(valid_directions)
    # Create a random out-edge on the origin and move the origin along it.
    match shift_direction:
        case "Right":
            grid.grid[grid.origin[0]][grid.origin[1]].right = 1
            grid.origin = [grid.origin[0]+1, grid.origin[1]]
        case "Bottom":
            grid.grid[grid.origin[0]][grid.origin[1]].bottom = 1
            grid.origin = [grid.origin[0], grid.origin[1]+1]
        case "Left":
            grid.grid[grid.origin[0]-1][grid.origin[1]].right = -1
            grid.origin = [grid.origin[0]-1, grid.origin[1]]
        case "Top":
            grid.grid[grid.origin[0]][grid.origin[1]-1].bottom = -1
            grid.origin = [grid.origin[0], grid.origin[1]-1]
        case _:
            raise ValueError("Invalid direction for shift_origin.")
    # Remove the existing out-edge of the new origin.
    if not (grid.origin[0] == grid.gridsize[0]-1):
        vector: int = grid.grid[grid.origin[0]][grid.origin[1]].right
        vector = 0 if (vector == 1) else vector
        grid.grid[grid.origin[0]][grid.origin[1]].right = vector
    if not (grid.origin[1] == grid.gridsize[1]-1):
        vector: int = grid.grid[grid.origin[0]][grid.origin[1]].bottom
        vector = 0 if (vector == 1) else vector
        grid.grid[grid.origin[0]][grid.origin[1]].bottom = vector
    if not (grid.origin[0] == 0):
        vector: int = grid.grid[grid.origin[0]-1][grid.origin[1]].right
        vector = 0 if (vector == -1) else vector
        grid.grid[grid.origin[0]-1][grid.origin[1]].right = vector
    if not (grid.origin[1] == 0):
        vector: int = grid.grid[grid.origin[0]][grid.origin[1]-1].bottom
        vector = 0 if (vector == -1) else vector
        grid.grid[grid.origin[0]][grid.origin[1]-1].bottom = vector
    