import pygame as pg
import numpy as np
import sys
import random
from os import path
from settings import *
from Terrain import *
from Robot import *



class Game:
    def __init__(self,difficulty,genSize):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.difficulty = difficulty
        self.generation = []
        self.genSize = genSize

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'maze.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.terrain = pg.sprite.Group()
        logicMaze = np.zeros((20,20),int)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    self.setTerrain(col,row)
                if tile == '1':
                    if(col < 20 and row < 20):
                        logicMaze[row][col] = 1
                    Wall(self, col, row)
                if tile == 'P':
                    Terrain(self,col,row,1)
                    for i in range(self.genSize):
                        self.generation.append(Player(self, col, row,i))
                if tile == 'F':
                    print('Finish Line')
        for i in range(self.genSize):
            self.generation[i].configure(logicMaze)

    def setTerrain(self,col, row):
        rand = random.randint(0,100)
        if (self.difficulty == 1):
            if (rand <= 80):
                Terrain(self,col,row,1)
            elif (rand > 80 and rand <= 90):
                Terrain(self,col,row,2)
            else:
                Terrain(self,col,row,3)



        if (self.difficulty == 2):
            if (rand <= 60):
                Terrain(self,col,row,1)
            elif (rand > 60 and rand <= 80):
                Terrain(self,col,row,2)
            else:
                Terrain(self,col,row,3)



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        #self.draw_grid()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
