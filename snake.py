import os.path
import random
import pygame
import sys
import pickle as pk1
import os.path as exists

pygame.init()
pygame.display.set_caption('Snake - Open Source SW')
# settings
grid_cell_size = 20
grid_size = 40
DIR_UP = [-1, 0]
DIR_DOWN = [1, 0]
DIR_LEFT = [0, -1]
DIR_RIGHT = [0, 1]
FPS = 60
snake_speed = 5

username = ""
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])


class Menu:
    def __init__(self, save_and_load, ranking):
        self.font = pygame.font.Font("assets/Bebas-Regular.ttf", 75)
        self.save_and_load = save_and_load
        self.ranking = ranking

    def check_buttons(self, buttons_list, mouse_position):
        for button in buttons_list:
            if mouse_position[0] in range(button.rect.left, button.rect.right) and \
                    mouse_position[1] in range(button.rect.top, button.rect.bottom):
                button.text = button.font.render(button.text_input, True, "White")
            else:
                button.text = button.font.render(button.text_input, True, "#a7843b")
            button.update(screen)

    def check_mouse(self, button, position):
        if position[0] in range(button.rect.left, button.rect.right) and \
                position[1] in range(button.rect.top, button.rect.bottom):
            return True
        return False

     
    def ingame_menu_loop(self, snake):
        pygame.display.set_caption("Ingame Menu")

        running = True
        while running:
            title = self.font.render("INGAME MENU", True, "#a7843b")
            title_rect = title.get_rect(center=(400, 100))
            mouse_position = pygame.mouse.get_pos()

            resume_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=250,
                                 text_input="RESUME", font=self.font)
            restart_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=400,
                                 text_input="RESTART", font=self.font)
            save_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=550,
                                    text_input="SAVE", font=self.font)
            exit_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=700,
                                 text_input="EXIT", font=self.font)

            screen.blit(title, title_rect)
            self.check_buttons([resume_button, restart_button, save_button, exit_button], mouse_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_mouse(resume_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        running = False
                    elif self.check_mouse(restart_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        play(resume=True)
                    elif self.check_mouse(save_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        self.save_and_load.save(snake)
                        play()
                    elif self.check_mouse(exit_button, mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def get_username(self, ranking, snake):
        font = pygame.font.SysFont(None, 35)
        text = ""
        inpt(screen, fpsClock, font, text, ranking, snake)

    loaded = False

    def main_menu_loop(self):
        pygame.display.set_caption("Main Menu")
        running = True
        while running:
            screen.blit(pygame.image.load("assets/menu_background.jpg"), (0, 0))
            title = self.font.render("MAIN MENU", True, "#a7843b")
            title_rect = title.get_rect(center=(400, 100))
            mouse_position = pygame.mouse.get_pos()

            play_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=250,
                                 text_input="PLAY", font=self.font)
            load_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=400,
                                 text_input="LOAD", font=self.font)
            ranking_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=550,
                                    text_input="RANKING", font=self.font)
            exit_button = Button(image=pygame.image.load("assets/button_rect.png"), x_pos=400, y_pos=700,
                                 text_input="EXIT", font=self.font)

            screen.blit(title, title_rect)
            self.check_buttons([play_button, load_button, ranking_button, exit_button], mouse_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_mouse(play_button, mouse_position):
                        pygame.display.set_caption("Snake")
                        running = False
                    elif self.check_mouse(exit_button, mouse_position):
                        pygame.quit()
                        sys.exit()
                    elif self.check_mouse(ranking_button, mouse_position):
                        self.ranking.get_ranking()
                    elif self.check_mouse(load_button, mouse_position):
                        self.loaded = True
                        pygame.display.set_caption("Snake")
                        running = False

            pygame.display.update()


class Button:
    def __init__(self, image, x_pos, y_pos, text_input, font):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "#a7843b")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)


class Snake:
    def __init__(self):
        self.snake = []
        self.direction = DIR_UP
        self.speed = 0

        #initial position y, x

        self.snake.append([19, 20])
        self.snake.append([18, 20])
        self.snake.append([20, 20])

        self.snake_grow = 0
        self.can_move = 1

        self.food_position = [0, 0]
        self.generate_food()

    def move(self):
        if (self.speed > snake_speed):
            self.speed = 0
            if (self.snake_grow):
                self.snake_grow = 0
            else:
                self.snake.pop(0)
            self.snake.append([self.snake[-1][0] + self.direction[0], self.snake[-1][1] + self.direction[1]])
            self.can_move = 1
        self.speed += 1
        if (self.snake[-1][0] < 0 or self.snake[-1][1] < 0 or self.snake[-1][0] >= 40 or self.snake[-1][1] >= 40):
            return 0
        snakeLength = len(self.snake)
        for i in range(0, snakeLength - 1):
            if self.snake[i] == self.snake[-1]:
                return 0
        return 1

    def display(self):
        for elem in self.snake:
            pygame.draw.circle(screen, (240, 230, 140), (elem[1] * grid_cell_size + 10, elem[0] * grid_cell_size + 10), 10)
        pygame.draw.circle(screen, (255, 0, 0), (self.food_position[1] * grid_cell_size + 10, self.food_position[0] * grid_cell_size + 10), 8)
    
    def set_direction(self, direction):
        if (self.direction[0] == direction[0] and self.direction[1] != direction[1]):
            return 1
        if (self.direction[1] == direction[1] and self.direction[0] != direction[0]):
            return 1
        if self.can_move:
            self.direction = direction
            self.can_move = 0
        return 1
    
    def generate_food(self):
        position_count = random.randint(0, (grid_size * grid_size) - len(self.snake))
        count = 0
        for y in range (grid_size):
            for x in range (grid_size):
                if (not is_array_in_list(self.snake, [y, x])):
                    if count == position_count:
                        self.food_position = [y, x]
                        y = grid_size
                        x = grid_size
                    count += 1

    def food_check(self):
        if (self.snake[-1][0] == self.food_position[0] and self.snake[-1][1] == self.food_position[1]):
            self.snake_grow = 1
            self.generate_food()


def is_array_in_list(list, array):
    for elem in list:
        if (elem[0] == array[0] and elem[1] == array[1]):
            return 1
    return 0 


def draw_background():
    tmp = 10
    for x in range(grid_size):
        for y in range(grid_size):
            pygame.draw.rect(screen, (0, 100 + tmp, 0), pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size))
            tmp *= -1
        tmp *= -1

def text_display(word,x,y):
    font = pygame.font.SysFont(None, 75)
    text = font.render("{}".format(word), True, "#a7843b")
    return screen.blit(text,text.get_rect(midtop=screen.get_rect().midtop))

def inpt(window, clock, font, text, ranking, snake):
    input_active = True
    window.fill(0)
    pygame.display.flip()
    one_time = True
    run = True
    while run:
        text_display("Please enter your name: ", 300, 400)
        if one_time == True:
            pygame.display.flip()
            one_time = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_active = True
                text = ""
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    run = False
                    ranking.set_ranking((len(snake.snake) - 3) * 100, text)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            window.fill(0)
            text_surf = font.render(text, True, "#a7843b")
            text_display("Please enter your name: ", 300, 400)
            window.blit(text_surf, text_surf.get_rect(center=window.get_rect().center))
            pygame.display.flip()

class Save_and_Load:
    def save(self, snake):
        with open('save_file.txt', 'wb') as f: pk1.dump(snake, f)

    def get_load_info(self):
        with open('save_file.txt', 'rb') as f: arrayname1 = pk1.load(f)
        return arrayname1

class Ranking:

    def __init__(self):
        self.ranking_list = []
        if os.path.exists("rankings.txt"):
            with open("rankings.txt") as file:
                for line in file:
                    line = line.replace('\n', '')
                    splited_line = line.split(';')
                    self.ranking_list.append([splited_line[0], int(splited_line[1])])

    def set_ranking(self, score, username):
        self.ranking_list.append([username, score])
        self.ranking_list = sorted(self.ranking_list, key = lambda x: int(x[1]))
        self.ranking_list.reverse()
        f = open("rankings.txt", 'w')
        for elem in self.ranking_list:
            f.write(elem[0].__str__())
            f.write(";")
            f.write(elem[1].__str__())
            f.write("\n")

    def get_ranking(self):
        if os.path.exists("rankings.txt"):
            screen.fill(0)
            text = ""
            for elem in self.ranking_list:
                text += elem[0] + ' ' + elem[1].__str__()
            pygame.display.flip()
            one_time = True
            run = True
            input_active = True
            font = pygame.font.SysFont(None, 45)
            while run:
                if one_time == True:
                    pygame.display.flip()
                    one_time = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        input_active = True
                    elif event.type == pygame.KEYDOWN and input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                            run = False
                    screen.fill(0)
                    text_display("RANKING", 0,0)
                    text = font.render("{}".format(self.ranking_list[0][0] + ' ' + str(self.ranking_list[0][1])), True, "#a7843b")
                    screen.blit(text, (320, 200))
                    if (len(self.ranking_list) > 1):
                        text = font.render("{}".format(self.ranking_list[1][0] + ' ' + str(self.ranking_list[1][1])), True, "#a7843b")
                        screen.blit(text, (320, 350))
                    if (len(self.ranking_list) > 2):
                        text = font.render("{}".format(self.ranking_list[2][0] + ' ' + str(self.ranking_list[2][1])), True, "#a7843b")
                        screen.blit(text, (320, 500))
                    pygame.display.flip()

def play(resume=False):
    ranking = Ranking()
    save_and_load = Save_and_Load()
    menu = Menu(save_and_load, ranking)
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
    play()