import pygame as pg
from settings import *
from Motor import *
from Camera import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,motorLvl,batteryLvl,cameraLvl):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE-6, TILESIZE-6))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.logicX = x
        self.logicY = y
        self.camera = None
        self.motor = Motor(motorLvl,batteryLvl)
        self.behavior = None
        self.possibleMoves = []
        self.currentTile = None
        self.cameraLvl = cameraLvl

    def configure(self,logicMaze):
        pos = (self.logicX,self.logicY)
        self.camera = Camera(logicMaze,pos,self.cameraLvl)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:

                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:

                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_terrain(self):
        hits = pg.sprite.spritecollide(self, self.game.terrain, False)
        if(len(hits) == 1):
            if (self.currentTile == None):
                self.currentTile = hits[0]

            elif(self.currentTile != hits[0]):
                self.motor.move(self.currentTile)
                self.currentTile = hits[0]

            if (self.currentTile.type > self.motor.type):
                print("robot no apto para el terreno, apagando...")
                self.motor.shutDown()

            self.logicX = self.currentTile.x
            self.logicY = self.currentTile.y
            self.camera.updateLocation(self.logicX,self.logicY)




    def update(self):
        if (self.motor.state):
            self.get_keys()
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
            self.collide_with_terrain()
            self.possibleMoves = self.camera.findNxtMove()
            print(self.possibleMoves)
