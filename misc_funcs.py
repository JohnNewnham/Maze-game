from py_objects import *
from random import choice, randint

def generatePlayerPos(gridsize: tuple[int, int]) -> list[int, int]:
    # Return a random position on the grid.
    return [randint(0, gridsize[0]-1), randint(0, gridsize[1]-1)]

def generateGoalPos(gridsize: tuple[int, int], player_pos: tuple[int, int]) -> tuple[int, int]:
    player_quadrant: Quadrant = checkQuadrant(gridsize, player_pos)
    while True:
        goal_pos: tuple[int, int] = (randint(0, gridsize[0]-1), randint(0, gridsize[1]-1))
        goal_quadrant: Quadrant = checkQuadrant(gridsize, goal_pos)
        if player_quadrant != goal_quadrant: return goal_pos

def checkQuadrant(gridsize: tuple[int, int], pos: tuple[int, int]) -> Quadrant:
    # Check which of the 4 corners of the grid the specified position is in.
    if (pos[0] <= gridsize[0]/2) and (pos[1] <= gridsize[1]/2): return Quadrant.TOP_LEFT
    if (pos[0] > gridsize[0]/2) and (pos[1] <= gridsize[1]/2): return Quadrant.TOP_RIGHT
    if (pos[0] <= gridsize[0]/2): return Quadrant.BOTTOM_LEFT
    return Quadrant.BOTTOM_RIGHT

def validMoveDirections(player_pos: tuple[int, int], grid: Grid) -> list[Direction]:
    # Obtains the valid directions for the player to move in.
    valid_directions: list[Direction] = []

    if player_pos[0] != 0:
        left_cell: Gridcell = grid.getCell((player_pos[0]-1, player_pos[1]))
        if left_cell.right: valid_directions.append(Direction.LEFT)
    if player_pos[1] != 0:
        top_cell: Gridcell = grid.getCell((player_pos[0], player_pos[1]-1))
        if top_cell.bottom: valid_directions.append(Direction.TOP)
    
    player_cell: Gridcell = grid.getCell(player_pos)
    if player_cell.bottom: valid_directions.append(Direction.BOTTOM)
    if player_cell.right: valid_directions.append(Direction.RIGHT)

    if len(valid_directions) == 0: raise Exception("No valid directions found for current player position!")
    return valid_directions

def generateGrid(gridsize: tuple[int, int]) -> Grid:
    grid = Grid(gridsize)
    for _ in range(10*gridsize[0]*gridsize[1]): shiftOrigin(grid)
    return grid

def shiftOrigin(grid: Grid) -> None:
    # Figure out valid direction by whether the origin is at thee edge of the grid.
    valid_directions: list[Direction] = []
    if not (grid.origin[0] == grid.gridsize[0]-1): valid_directions.append(Direction.RIGHT)
    if not (grid.origin[1] == grid.gridsize[1]-1): valid_directions.append(Direction.BOTTOM)
    if not (grid.origin[0] == 0): valid_directions.append(Direction.LEFT)
    if not (grid.origin[1] == 0): valid_directions.append(Direction.TOP)
    # Pick a valid direction.
    shift_direction: Direction = choice(valid_directions)
    # Create a random out-edge on the origin and move the origin along it.
    match shift_direction:
        case Direction.RIGHT:
            grid.grid[grid.origin[0]][grid.origin[1]].right = 1
            grid.origin = [grid.origin[0]+1, grid.origin[1]]
        case Direction.BOTTOM:
            grid.grid[grid.origin[0]][grid.origin[1]].bottom = 1
            grid.origin = [grid.origin[0], grid.origin[1]+1]
        case Direction.LEFT:
            grid.grid[grid.origin[0]-1][grid.origin[1]].right = -1
            grid.origin = [grid.origin[0]-1, grid.origin[1]]
        case Direction.TOP:
            grid.grid[grid.origin[0]][grid.origin[1]-1].bottom = -1
            grid.origin = [grid.origin[0], grid.origin[1]-1]
        case _:
            raise ValueError("Invalid direction for shiftOrigin.")
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
    