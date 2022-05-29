from snake_settings import *
from snake_player_object import *
import snake_menus
from snake_save_and_ranking import *

pygame.init()
pygame.display.set_caption('Snake - Open Source SW')

def draw_background():
    tmp = 10
    for x in range(single_player_grid_width):
        for y in range(single_player_grid_height):
            pygame.draw.rect(screen, (0, 100 + tmp, 0), pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size))
            tmp *= -1
        tmp *= -1


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


def auto_play(resume=False):
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
        next_pos_up = (snake.get_snake_position()[1], snake.get_snake_position()[0] - 1)
        next_pos_down = (snake.get_snake_position()[1], snake.get_snake_position()[0] + 1)
        next_pos_right = (snake.get_snake_position()[1] + 1, snake.get_snake_position()[0])
        next_pos_left = (snake.get_snake_position()[1] - 1, snake.get_snake_position()[0])

        manhattan_distance_up = abs(snake.food_position[1] - next_pos_up[0]) + \
                                abs(snake.food_position[0] - next_pos_up[1])
        manhattan_distance_down = abs(snake.food_position[1] - next_pos_down[0]) + \
                                  abs(snake.food_position[0] - next_pos_down[1])
        manhattan_distance_right = abs(snake.food_position[1] - next_pos_right[0]) + \
                                   abs(snake.food_position[0] - next_pos_right[1])
        manhattan_distance_left = abs(snake.food_position[1] - next_pos_left[0]) + \
                                  abs(snake.food_position[0] - next_pos_left[1])

        j, i = min((j, i) for (i, j) in enumerate([manhattan_distance_up, manhattan_distance_down,
                                                   manhattan_distance_right, manhattan_distance_left]))

        if (i == 0):
            if snake.direction != DIR_DOWN:
                running = snake.set_direction(DIR_UP)
            else:
                running = snake.set_direction(DIR_RIGHT)
        elif (i == 1):
            if snake.direction != DIR_UP:
                running = snake.set_direction(DIR_DOWN)
            else:
                running = snake.set_direction(DIR_LEFT)
        elif (i == 2):
            if snake.direction != DIR_LEFT:
                running = snake.set_direction(DIR_RIGHT)
            else:
                running = snake.set_direction(DIR_UP)
        else:
            if snake.direction != DIR_RIGHT:
                running = snake.set_direction(DIR_LEFT)
            else:
                running = snake.set_direction(DIR_DOWN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
    play()