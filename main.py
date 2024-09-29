import pygame
from py_objects import *
from misc_funcs import *

debug: bool = False

def drawMaze() -> None:
    for x, y in grid.iterable():
        gridcell: Gridcell = grid.getCell((x, y))
        # Each cell contains information on whether there is not a wall to its right and bottom only.
        if (x==0): display.blit(left_img, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
        if (y==0): display.blit(top_img, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
        if not gridcell.right: display.blit(right_img, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
        if not gridcell.bottom: display.blit(bottom_img, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))

        if debug:
            match gridcell.right:
                case 1: display.blit(right_arrow, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
                case -1: display.blit(left_arrow, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
            match gridcell.bottom:
                case 1: display.blit(bottom_arrow, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
                case -1: display.blit(top_arrow, (gridsquare_size*x-gridsquare_size/2, gridsquare_size*y-gridsquare_size/2))
    display.blit(goal_img, (gridsquare_size*goal_pos[0], gridsquare_size*goal_pos[1]))
    display.blit(ghost_img, (gridsquare_size*grid.origin[0], gridsquare_size*grid.origin[1]))
    display.blit(player_img, (gridsquare_size*player_pos[0], gridsquare_size*player_pos[1]))
    display.blit(text_surface, ((display.get_width() - text_surface.get_width())/2,
                gridsquare_size*gridsize[1]+(gridsquare_size - text_surface.get_height())/2))



if __name__ == "__main__":

    # Import images.
    left_img: pygame.Surface = pygame.image.load("images/left1.png")
    top_img: pygame.Surface = pygame.image.load("images/top1.png")
    right_img: pygame.Surface = pygame.image.load("images/right1.png")
    bottom_img: pygame.Surface = pygame.image.load("images/bottom1.png")
    player_img: pygame.Surface = pygame.image.load("images/player.png")
    goal_img: pygame.Surface = pygame.image.load("images/goal.png")
    ghost_img: pygame.Surface = pygame.image.load("images/ghost.png")

    if debug:
        left_arrow: pygame.Surface = pygame.image.load("images/left_arrow.png")
        top_arrow: pygame.Surface = pygame.image.load("images/top_arrow.png")
        right_arrow: pygame.Surface = pygame.image.load("images/right_arrow.png")
        bottom_arrow: pygame.Surface = pygame.image.load("images/bottom_arrow.png")

    # Set constants for the game.
    gridsize: tuple[int, int] = (10,10)
    gridsquare_size: int = 64
    
    grid: Grid = generateGrid(gridsize)
    movement: Movement = Movement()
    W_pressed: bool = False
    A_pressed: bool = False
    S_pressed: bool = False
    D_pressed: bool = False
    score: int = 0
    player_pos: list[int, int] = generatePlayerPos(gridsize)
    goal_pos: tuple[int, int]  = generateGoalPos(gridsize, player_pos)
    valid_directions: list[Direction] = []

    pygame.init()

    font: pygame.font = pygame.font.Font("ZTTalk-SemiBold.ttf", gridsquare_size*3//4)
    text_surface: pygame.Surface = font.render(f"Score: {score}", False, (0, 0, 0))

    display: pygame.Surface = pygame.display.set_mode((gridsize[0]*gridsquare_size, (gridsize[1]+1)*gridsquare_size))
    pygame.display.set_caption("Maze game")

    # Enter gameloop.
    running: bool = True
    while running:
        # Set background to white and draw maze.
        display.fill((255, 255, 255))
        text_surface = font.render(f"Score: {score}", False, (0, 0, 0))
        drawMaze()

        movement.setAllFalse()
        valid_directions = validMoveDirections(player_pos, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

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
        if not movement: movement.setAllFalse()            

        # Move the player.
        if movement.left and (Direction.LEFT in valid_directions): 
            player_pos[0] -= 1
        elif movement.right and (Direction.RIGHT in valid_directions): 
            player_pos[0] += 1
        elif movement.top and (Direction.TOP in valid_directions): 
            player_pos[1] -= 1
        elif movement.bottom and (Direction.BOTTOM in valid_directions): 
            player_pos[1] += 1
        else:
            # Disable movement if the direction input was not valid.
            movement.setAllFalse()  

        if movement:
            # If only one key is input, do things.
            for _ in range(4): shiftOrigin(grid)
            score += 1

            # Check win condition.
            if tuple(player_pos) == goal_pos:
                running = False
                print(f"You won! Your final score is: {score}")

            # Debug prints.
            if debug: 
                print(f"Origin: {grid.origin}")
                print(f"Score: {score}")

        pygame.display.update()