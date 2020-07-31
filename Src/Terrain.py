import pygame as pg
from settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image.fill(RED)


class Terrain(pg.sprite.Sprite):
    def __init__(self, game, x, y,type):
        self.groups = game.all_sprites, game.terrain
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.type = type

        if (type == 1):
            self.image.fill(BLACK)
        if (type == 2):
            self.image.fill(PURPLE)
        elif (type == 3):
            self.image.fill(GREEN)




