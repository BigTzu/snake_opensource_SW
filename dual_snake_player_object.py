from turtle import width
from snake_settings import *

class DualSnake:
    def __init__(self):
        self.snakeOne = []
        self.snakeTwo = []
        self.directionOne = DIR_DOWN
        self.directionTwo = DIR_UP
        self.speed = 0

        #initial position y, x

        self.snakeOne.append([1, 0])
        self.snakeOne.append([2, 0])
        self.snakeOne.append([3, 0])

        self.snakeTwo.append([dual_player_grid_height - 1, dual_player_grid_width - 1])
        self.snakeTwo.append([dual_player_grid_height - 2, dual_player_grid_width - 1])
        self.snakeTwo.append([dual_player_grid_height - 3, dual_player_grid_width - 1])

        self.snakeOne_grow = 0
        self.snakeTwo_grow = 0

        self.can_move = 1

        self.foodOne_position = [-1, -1]
        self.foodTwo_position = [-1, -1]
        self.generate_food(0) #0 generate both foods

    def move(self):
        if (self.speed > snake_speed):
            self.speed = 0
            if (self.snakeOne_grow):
                self.snakeOne_grow = 0
            else:
                self.snakeOne.pop(0)
            self.speed = 0
            if (self.snakeTwo_grow):
                self.snakeTwo_grow = 0
            else:
                self.snakeTwo.pop(0)
            self.snakeOne.append([self.snakeOne[-1][0] + self.directionOne[0], self.snakeOne[-1][1] + self.directionOne[1]])
            self.snakeTwo.append([self.snakeTwo[-1][0] + self.directionTwo[0], self.snakeTwo[-1][1] + self.directionTwo[1]])
            self.can_move = 1
        self.speed += 1
        if (self.snakeOne[-1][0] < 0 or self.snakeOne[-1][1] < 0 or self.snakeOne[-1][0] >= dual_player_grid_height or self.snakeOne[-1][1] >= dual_player_grid_width):
            return 0
        snakeLength = len(self.snakeOne)
        for i in range(0, snakeLength - 1):
            if self.snakeOne[i] == self.snakeOne[-1]:
                return 0
        return 1

    def display(self):
        for elem in self.snakeOne:
            pygame.draw.circle(screen, snake_one_color, (elem[1] * grid_cell_size + 10, elem[0] * grid_cell_size + 10), 10)
        for elem in self.snakeTwo:
            pygame.draw.circle(screen, snake_two_color, (elem[1] * grid_cell_size + 10, elem[0] * grid_cell_size + 10), 10)
        pygame.draw.circle(screen, (255, 0, 0), (self.foodOne_position[1] * grid_cell_size + 10, self.foodOne_position[0] * grid_cell_size + 10), 8)
        pygame.draw.circle(screen, (255, 0, 0), (self.foodTwo_position[1] * grid_cell_size + 10, self.foodTwo_position[0] * grid_cell_size + 10), 8)
    
    def set_direction(self, player, direction):
        if (player == 1):
            if (self.directionOne[0] == direction[0] and self.directionOne[1] != direction[1]):
                return 1
            if (self.directionOne[1] == direction[1] and self.directionOne[0] != direction[0]):
                return 1
            if self.can_move:
                self.directionOne = direction
                self.can_move = 0
            return 1
        elif(player == 2):
            if (self.directionTwo[0] == direction[0] and self.directionTwo[1] != direction[1]):
                return 1
            if (self.directionTwo[1] == direction[1] and self.directionTwo[0] != direction[0]):
                return 1
            if self.can_move:
                self.directionTwo = direction
                self.can_move = 0
            return 1
        return 0
    
    def generate_food(self, food_number):
        if (food_number == 1 or not food_number):
            position_count = random.randint(0, (dual_player_grid_width * dual_player_grid_height) - len(self.snakeOne) - len(self.snakeTwo) - 1) #-1 for the other food
            count = 0
            for y in range (dual_player_grid_height):
                for x in range (dual_player_grid_width):
                    if (not is_array_in_list(self.snakeOne, [y, x]) and not is_array_in_list(self.snakeTwo, [y, x]) and not is_array_equal(self.foodTwo_position, [y, x])):
                        if count == position_count:
                            self.foodOne_position = [y, x]
                            y = dual_player_grid_height
                            x = dual_player_grid_width
                        count += 1
        if (food_number == 2 or not food_number):
            position_count = random.randint(0, (dual_player_grid_width * dual_player_grid_height) - len(self.snakeOne) - len(self.snakeTwo) - 1) #-1 for the other food
            count = 0
            for y in range (dual_player_grid_height):
                for x in range (dual_player_grid_width):
                    if (not is_array_in_list(self.snakeOne, [y, x]) and not is_array_in_list(self.snakeTwo, [y, x]) and not is_array_equal(self.foodOne_position, [y, x])):
                        if count == position_count:
                            self.foodTwo_position = [y, x]
                            y = dual_player_grid_height
                            x = dual_player_grid_width
                        count += 1

    def food_check(self):
        if (self.snakeOne[-1][0] == self.foodOne_position[0] and self.snakeOne[-1][1] == self.foodOne_position[1]):
            self.snakeOne_grow = 1
            self.generate_food(1)
        elif (self.snakeOne[-1][0] == self.foodTwo_position[0] and self.snakeOne[-1][1] == self.foodTwo_position[1]):
            self.snakeOne_grow = 1
            self.generate_food(2)
        if (self.snakeTwo[-1][0] == self.foodOne_position[0] and self.snakeTwo[-1][1] == self.foodOne_position[1]):
            self.snakeTwo_grow = 1
            self.generate_food(1)
        elif (self.snakeTwo[-1][0] == self.foodTwo_position[0] and self.snakeTwo[-1][1] == self.foodTwo_position[1]):
            self.snakeTwo_grow = 1
            self.generate_food(2)

def is_array_equal(arr1, arr2):
    len_arr1 = len(arr1)
    len_arr2 = len(arr2)

    if len_arr1 != len_arr2:
        return 0
    for i in range(len_arr1):
        if (arr1[i] != arr2[i]):
            return 0
    return 1
    

def is_array_in_list(list, array):
    for elem in list:
        if (elem[0] == array[0] and elem[1] == array[1]):
            return 1
    return 0