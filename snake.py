from operator import truediv
from unittest import runner
from snake_settings import *
from snake_player_object import *
from dual_snake_player_object import *
import snake_menus
from snake_save_and_ranking import *
from algo import *


pygame.init()
pygame.display.set_caption('Snake - Open Source SW')

def draw_dual_background():
    tmp = 10
    for x in range(dual_player_grid_width):
        for y in range(dual_player_grid_height):
            pygame.draw.rect(screen, (0, 100 + tmp, 0), pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size))
            tmp *= -1
        tmp *= -1

def draw_background():
    tmp = 10
    for x in range(single_player_grid_width):
        for y in range(single_player_grid_height):
            pygame.draw.rect(screen, (0, 100 + tmp, 0), pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size))
            tmp *= -1
        tmp *= -1

def dualPlay(resume=False):
    ranking = Ranking()
    save_and_load = Save_and_Load()
    menu = snake_menus.Menu(save_and_load, ranking)
    if resume is False:
        menu.main_menu_loop()
    screen = pygame.display.set_mode([1600, 800])

    screen.fill((240, 230, 140))
    dualSnake = DualSnake()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    running = dualSnake.set_direction(1, DIR_UP)
                elif event.key == pygame.K_DOWN:
                    running = dualSnake.set_direction(1, DIR_DOWN)
                elif event.key == pygame.K_LEFT:
                    running = dualSnake.set_direction(1, DIR_LEFT)
                elif event.key == pygame.K_RIGHT:
                    running = dualSnake.set_direction(1, DIR_RIGHT)
                if event.key == pygame.K_z:
                    running = dualSnake.set_direction(2, DIR_UP)
                elif event.key == pygame.K_s:
                    running = dualSnake.set_direction(2, DIR_DOWN)
                elif event.key == pygame.K_q:
                    running = dualSnake.set_direction(2, DIR_LEFT)
                elif event.key == pygame.K_d:
                    running = dualSnake.set_direction(2, DIR_RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    menu.special_mode_menu_loop("dual")
        if (not running):
            break

        draw_dual_background()
        running = dualSnake.move()

        dualSnake.food_check()
        dualSnake.display()

        pygame.display.flip()
        fpsClock.tick(FPS)
    pygame.quit()
    sys.exit()

def play(resume=False):
    ranking = Ranking()
    save_and_load = Save_and_Load()
    menu = snake_menus.Menu(save_and_load, ranking)
    if resume is False:
        menu.main_menu_loop()
    screen.fill((240, 230, 140))
    if menu.loaded is True:
        snake = save_and_load.get_load_info()
    else:
        snake = Snake()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    running = snake.set_direction(DIR_UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    running = snake.set_direction(DIR_DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    running = snake.set_direction(DIR_LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    running = snake.set_direction(DIR_RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    menu.ingame_menu_loop(snake)

        if (not running):
            break

        draw_background()
        running = snake.move()
        if running == 0:
            menu.get_username(ranking, snake)

        snake.food_check()
        snake.display()

        pygame.display.flip()
        fpsClock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    #play()
    play_algo()