from snake_settings import *
from snake_player_object import *
import snake_menus
from snake_save_and_ranking import *

def draw_background():
    tmp = 10
    for x in range(single_player_grid_width):
        for y in range(single_player_grid_height):
            pygame.draw.rect(screen, (0, 100 + tmp, 0), pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size))
            tmp *= -1
        tmp *= -1

def play_algo(resume=False):
    ranking = Ranking()
    save_and_load = Save_and_Load()
    menu = snake_menus.Menu(save_and_load, ranking)
    if resume is False:
        menu.main_menu_loop()

    previous_snake_pos = [0,0]
    screen.fill((240, 230, 140))
    snake = Snake()
    running = True
    sequence = False
    sequence_two = False
    enabled = False
    while running:
        if snake.get_position()[0] == 0 and enabled == False:
            enabled = True
            running = snake.set_direction(DIR_LEFT)

        if enabled == True:
            if snake.get_position()[1] == single_player_grid_width - 1 and previous_snake_pos[0] <= snake.get_position()[0] and snake.get_position()[0] != 0:
                running = snake.set_direction(DIR_UP)
            if snake.get_position()[1] == single_player_grid_width - 1 and snake.get_position()[0] == 0:
                running = snake.set_direction(DIR_LEFT)
            if snake.get_position()[0] == 0 and snake.get_position()[1] == 0:
                running = snake.set_direction(DIR_DOWN)
            if sequence == True:
                running = snake.set_direction(DIR_DOWN)
                sequence = False

            if snake.get_position()[0] == 1 and sequence == False and snake.get_position()[1] != 0:
                running = snake.set_direction(DIR_RIGHT)
                sequence = True

            if sequence_two == True:
                running = snake.set_direction(DIR_UP)
                sequence_two = False

            if snake.get_position()[0] == single_player_grid_height - 1 and sequence_two == False:
                running = snake.set_direction(DIR_RIGHT)
                sequence_two = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.special_mode_menu_loop("auto")

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
        previous_snake_pos = snake.get_position()

    pygame.quit()
    sys.exit()