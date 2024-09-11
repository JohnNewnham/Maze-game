from typing import Generator

class Gridcell:
    def __init__(self, left: bool=True, top: bool=True, right: bool=True, bottom: bool=True) -> None:
        self.left: bool = left
        self.top: bool = top
        self.right: bool = right
        self.bottom: bool = bottom

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
        self.__grid: list[list[Gridcell]] = [[Gridcell() for _ in range(gridsize[0])] for _ in range(gridsize[1])]
        self.__gridsize: tuple[int, int] = gridsize

    def get_cell(self, coords: tuple[int, int]) -> (Gridcell | None):
        # Coords must be less than gridsize as indexing starts at 0.
        if (coords[0] >= self.__gridsize[0]) or (coords[1] >= self.__gridsize[1]) or (len(coords) != 2):
            return None
        return self.__grid[coords[0]][coords[1]]
    
    def set_cell(self, gridcell: Gridcell, coords: tuple[int, int]) -> None:
        # Coords must be less than gridsize as indexing starts at 0.
        if (coords[0] >= self.__gridsize[0]) or (coords[1] >= self.__gridsize[1]) or (len(coords) != 2):
            return
        self.__grid[coords[0]][coords[1]] = gridcell

    def iterable(self) -> Generator[tuple[int, int], None, None]:
        # Returns the coordinates of each cell one at a time as a tuple.
        coords: list[int, int] = [0, 0]
        for x_coord in range(self.__gridsize[0]):
            for y_coord in range(self.__gridsize[1]):
                yield (coords[0], coords[1])
                y_coord += 1
            x_coord += 1