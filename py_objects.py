from typing import Generator

class Gridcell:
    def __init__(self, right: int=1, bottom: int=1) -> None:
        # Despite each cell being adjacent to 4 other cells you only need to store information for 2 of the walls as there is duplicate data.
        # Walls for top and left edge handled separately.
        # Use an int to store direction for a root directed tree.
        self.right: int = right
        self.bottom: int = bottom

class Movement:
    def __init__(self, left: bool=False, top: bool=False, right: bool=False, bottom: bool=False) -> None:
        self.left: bool = left
        self.top: bool = top
        self.right: bool = right
        self.bottom: bool = bottom

    def set_false(self) -> None:
        self.left = False
        self.top = False
        self.right = False
        self.bottom = False

    def one_direction(self) -> bool:
        direction_num = int(self.left) + int(self.top) + int(self.right) + int(self.bottom)
        return (direction_num == 1)

class Grid:
    def __init__(self, gridsize: tuple[int, int]) -> None:

        grid = []
        for i in range(gridsize[0]):
            grid.append([])
            for j in range(gridsize[1]):
                if (i == gridsize[0]-1):
                    if (j == gridsize[1]-1):
                        grid[i].append(Gridcell(right=0, bottom=0))
                    else:
                        grid[i].append(Gridcell(right=0, bottom=1))
                else:
                    grid[i].append(Gridcell(right=1, bottom=0))

        self.__grid: list[list[Gridcell]] = grid
        self.gridsize: tuple[int, int] = gridsize
        self.origin: list[int, int] = list(gridsize)

    def get_cell(self, coords: tuple[int, int]) -> (Gridcell | None):
        # Coords must be less than gridsize as indexing starts at 0.
        if (coords[0] >= self.gridsize[0]) or (coords[1] >= self.gridsize[1]) or (len(coords) != 2):
            return None
        return self.__grid[coords[0]][coords[1]]
    
    def set_cell(self, gridcell: Gridcell, coords: tuple[int, int]) -> None:
        # Coords must be less than gridsize as indexing starts at 0.
        if (coords[0] >= self.gridsize[0]) or (coords[1] >= self.gridsize[1]) or (len(coords) != 2):
            return
        self.__grid[coords[0]][coords[1]] = gridcell

    def iterable(self) -> Generator[tuple[int, int], None, None]:
        # Returns the coordinates of each cell one at a time as a tuple.
        for x_coord in range(self.gridsize[0]):
            for y_coord in range(self.gridsize[1]):
                yield (x_coord, y_coord)
                y_coord += 1
            x_coord += 1