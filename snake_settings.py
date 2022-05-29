import os.path
import random
import pygame
import sys
import pickle as pk1
import os.path as exists

# settings
grid_cell_size = 20
single_player_grid_width = 40
single_player_grid_height = 40
dual_player_grid_width = 80
dual_player_grid_height = 40

snake_one_color = (167, 199, 231)
snake_two_color = (240, 230, 140)
# grid_size = 40
DIR_UP = [-1, 0]
DIR_DOWN = [1, 0]
DIR_LEFT = [0, -1]
DIR_RIGHT = [0, 1]
FPS = 60
snake_speed = 5

os.environ['SDL_VIDEO_WINDOW_POS'] = str(50) + "," + str(50)
username = ""
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])