import pygame
from py_objects import Gridcell, Grid, Movement
from misc_funcs import generate_grid, shift_origin

debug: bool = False

def draw_maze() -> None:
    for x, y in grid.iterable():
        gridcell: Gridcell = grid.get_cell((x, y))
        # Each cell contains information on whether there is not a wall to its right and bottom only.
        if (x==0): display.blit(left_img, (64*x-32, 64*y-32))
        if (y==0): display.blit(top_img, (64*x-32, 64*y-32))
        if not gridcell.right: display.blit(right_img, (64*x-32, 64*y-32))
        if not gridcell.bottom: display.blit(bottom_img, (64*x-32, 64*y-32))

        if debug:
            match gridcell.right:
                case 1: display.blit(right_arrow, (64*x-32, 64*y-32))
                case -1: display.blit(left_arrow, (64*x-32, 64*y-32))
            match gridcell.bottom:
                case 1: display.blit(bottom_arrow, (64*x-32, 64*y-32))
                case -1: display.blit(top_arrow, (64*x-32, 64*y-32))



if __name__ == "__main__":

    # Import images.
    left_img = pygame.image.load("images/left1.png")
    top_img = pygame.image.load("images/top1.png")
    right_img = pygame.image.load("images/right1.png")
    bottom_img = pygame.image.load("images/bottom1.png")

    if debug:
        left_arrow = pygame.image.load("images/left_arrow.png")
        top_arrow = pygame.image.load("images/top_arrow.png")
        right_arrow = pygame.image.load("images/right_arrow.png")
        bottom_arrow = pygame.image.load("images/bottom_arrow.png")

    # Set constants for the game.
    gridsize: tuple[int, int] = (10,10)
    gridsquare_size: int = 64
    
    grid: Grid = generate_grid(gridsize)
    movement: Movement = Movement()
    W_pressed = False
    A_pressed = False
    S_pressed = False
    D_pressed = False

    pygame.init()

    display = pygame.display.set_mode((gridsize[0]*gridsquare_size, gridsize[1]*gridsquare_size))
    pygame.display.set_caption("Maze game")

    # Enter gameloop.
    running = True
    while running:
        # Set background to white and draw maze.
        display.fill((255, 255, 255))
        draw_maze()

        movement.set_false()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Only move once per key press, don't move multiple times if the key is held.
                if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                    if not W_pressed: movement.top = True
                    W_pressed = True
                elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                    if not A_pressed: movement.left = True
                    A_pressed = True
                elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
                    if not S_pressed: movement.bottom = True
                    S_pressed = True
                elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                    if not D_pressed: movement.right = True
                    D_pressed = True

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                    W_pressed = False
                elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                    A_pressed = False
                elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
                    S_pressed = False
                elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                    D_pressed = False

        # If multiple keys are pressed simultaneously, don't move.
        if not movement.one_direction(): movement.set_false()

        # Move the player.
        if movement.left: 
            if debug:
                shift_origin(grid)
                print(grid.origin)
            print("Left")
        if movement.right: print("Right")
        if movement.top: print("Top")
        if movement.bottom: print("Bottom")

        pygame.display.update()