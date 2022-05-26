from snake_settings import *

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
        position_count = random.randint(0, (single_player_grid_width * single_player_grid_height) - len(self.snake))
        count = 0
        for y in range (single_player_grid_height):
            for x in range (single_player_grid_width):
                if (not is_array_in_list(self.snake, [y, x])):
                    if count == position_count:
                        self.food_position = [y, x]
                        y = single_player_grid_height
                        x = single_player_grid_width
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