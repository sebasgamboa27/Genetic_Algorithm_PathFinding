import pygame as pg
import threading
import time
from settings import *
from Motor import *
from Camera import *
from DNA import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,id,genes=None):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.logicX = x
        self.logicY = y
        if(genes==None):
            self.behavior = DNA()
        else:
            self.behavior = DNA(genes)
        self.camera = None
        self.motor = Motor(self,self.behavior.array[4][0],self.behavior.array[4][1])
        self.possibleMoves = []
        self.currentTile = None
        self.cameraLvl = self.behavior.array[4][2]
        self.nxtMove = "top"
        self.pastMove = ""
        self.moveThread = threading.Thread(target = self.movement)
        self.batteryThread = threading.Thread(target = self.consume)
        self.id = id
        self.fitness = 0
        self.won = False


    def CalculateFitness(self):     # The closer it is, the better it's fitness is.
        '''dist = self.game.Distance(self.x, self.game.finish.x, self.y, self.game.finish.y)
        self.fitness = self.game.Remap(0, WIDTH, 1, 0, dist)
        if(self.fitness<0):
            self.fitness = -self.fitness'''
        self.fitness = self.game.Distance(self.x, self.game.finish.x, self.y, self.game.finish.y)


    def consume(self):
        self.motor.consumeBattery(0.5)
        time.sleep(1)
        print(self.motor.battery.batteryPercentage)

    def configure(self,logicMaze):
        pos = (self.logicX,self.logicY)
        self.camera = Camera(logicMaze,pos,self.cameraLvl)
        #self.moveThread = threading.Thread(target=self.movement)
        #self.batteryThread = threading.Thread(target=self.consume)
        self.moveThread.start()
        self.batteryThread.start()

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

    def advance(self,case):
        self.vx, self.vy = 0, 0

        if case == 1:
            self.vx = -PLAYER_SPEED
        if case == 2:
            self.vx = PLAYER_SPEED
        if case == 3:
            self.vy = -PLAYER_SPEED
        if case == 4:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    def movement(self):

        while(self.motor):

            if not self.motor.state:
                break

            if(self.logicX >= 19 and self.logicY <= 1):
                self.won = true
                self.motor.shutDown()
                print('ganeeeee')

            iteraciones = 0
            if(self.nxtMove == "top"):
                newY = self.y - 35
                while(self.y != newY):
                    self.advance(3)
                    iteraciones += 1
                    if(iteraciones>= 500):
                        break
                self.pastMove = "top"


            elif (self.nxtMove == "down"):
                newY = self.y + 35
                while (self.y != newY):
                    self.advance(4)

                    iteraciones += 1
                    if (iteraciones >= 500):
                        break

                self.pastMove = "down"

            elif (self.nxtMove == "left"):
                newX = self.x - 35
                while (self.x != newX):
                    self.advance(1)
                    iteraciones += 1
                    if (iteraciones >= 500):
                        break

                self.pastMove = "left"

            elif (self.nxtMove == "right"):
                newX = self.x + 35
                while (self.x != newX):
                    self.advance(2)
                    iteraciones += 1
                    if (iteraciones >= 500):
                        break
                        
                self.pastMove = "right"

            self.nxtMove = self.behavior.choosePath(self.possibleMoves,self.pastMove)[0]

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
                self.motor.shutDown()
                print("robot no apto para el terreno, apagando...")

            self.logicX = self.currentTile.x
            self.logicY = self.currentTile.y
            self.camera.updateLocation(self.logicX,self.logicY)




    def update(self):
        if (self.motor.state):
            self.x += self.vx
            self.y += self.vy
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
            self.collide_with_terrain()
            self.possibleMoves = self.camera.findNxtMove()
            self.vx, self.vy = 0, 0


