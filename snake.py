import random
import pygame
import sys

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
snake_speed = 3

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])


class Menu:
    def __init__(self):
        self.font = pygame.font.Font("assets/Bebas-Regular.ttf", 75)

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

    def ingame_menu_loop(self):
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
                    elif self.check_mouse(exit_button, mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

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
        self.speed += 1
        if (self.snake[-1][0] < 0 or self.snake[-1][1] < 0 or self.snake[-1][0] >= 40 or self.snake[-1][1] >= 40):
            return 0
        return 1

    def display(self):
        for elem in self.snake:
            pygame.draw.circle(screen, (240, 230, 140), (elem[1] * grid_cell_size + 10, elem[0] * grid_cell_size + 10), 10)
        pygame.draw.circle(screen, (255, 0, 0), (self.food_position[1] * grid_cell_size + 10, self.food_position[0] * grid_cell_size + 10), 8)
    
    def set_direction(self, direction):
        if (self.direction[0] == direction[0] and self.direction[1] != direction[1]):
            return 0
        if (self.direction[1] == direction[1] and self.direction[0] != direction[0]):
            return 0
        self.direction = direction
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


def play(resume=False):
    menu = Menu()
    if resume is False:
        menu.main_menu_loop()

    screen.fill((240, 230, 140))
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
                    menu.ingame_menu_loop()

        if (not running):
            break

        draw_background()
        running = snake.move()
        snake.food_check()
        snake.display()

        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        pygame.display.flip()
        fpsClock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    play()