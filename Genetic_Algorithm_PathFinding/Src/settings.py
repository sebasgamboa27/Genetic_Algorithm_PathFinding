import pygame
from pygame.locals import *
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (11,255,1)
RED = (254,0,0)
YELLOW = (255, 255, 0)
BLUE = (70, 173, 212)
PURPLE = (254,0,246)

# game settings
WIDTH = 1400   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 730  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Genetic Maze"
BGCOLOR = BLACK

TILESIZE = 35
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 1


#Title Images
TITLEIMAGE = pygame.image.load('GeneticMaze.jpg')
GENERACIONIMAGE = pygame.image.load('Generacion.jpg')
ROBOTSIMAGE = pygame.image.load('Robots.jpg')
FINISHEDIMAGE = pygame.image.load('Resueltos.jpg')
AVERAGE = pygame.image.load('average.jpg')
LOWEST = pygame.image.load('lowest.jpg')
PARENTS = pygame.image.load('parents.jpg')
BEST = pygame.image.load('best.jpg')