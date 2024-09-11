import pygame
from py_objects import Gridcell, Grid, Movement
from generate_grid import generate_grid

def main():
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

    # Enter gameloop.
    running = True
    while running:
        # Set background to white.
        display.fill((255, 255, 255))

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
        if movement.left: print("Left")
        if movement.right: print("Right")
        if movement.top: print("Top")
        if movement.bottom: print("Bottom")

        pygame.display.update()



if __name__ == "__main__":
    main()