from ast import Return
from pickletools import UP_TO_NEWLINE
from turtle import speed
import pygame
import random
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
        if (snake.direction[0] == direction[0] and snake.direction[1] != direction[1]):
            return 0
        if (snake.direction[1] == direction[1] and snake.direction[0] != direction[0]):
            return 0
        snake.direction = direction 
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

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode([800, 800])

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

    draw_background()
    running = snake.move()
    snake.food_check()
    snake.display()

    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()