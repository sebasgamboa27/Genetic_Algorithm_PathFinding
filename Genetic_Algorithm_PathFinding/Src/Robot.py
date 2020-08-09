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
        if (genes == None):
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
        self.Parents = [['None'],['None']]

    def CalculateFitness(self):  # The closer it is, the better it's fitness is.
        '''dist = self.game.Distance(self.x, self.game.finish.x, self.y, self.game.finish.y)
        self.fitness = self.game.Remap(0, WIDTH, 1, 0, dist)
        if(self.fitness<0):
            self.fitness = -self.fitness'''
        self.fitness = self.game.Distance(self.logicX, self.game.finish.x, self.logicY, self.game.finish.y)

    def consume(self):
        while(self.motor.state):
            self.motor.consumeBattery(5)
            time.sleep(1)

    def configure(self,logicMaze):
        pos = (self.logicX,self.logicY)
        self.camera = Camera(logicMaze,pos,self.cameraLvl)
        self.moveThread.start()
        self.batteryThread.start()


    def movement(self):
        while(self.motor.state):
            if self.logicX >= 18 and self.logicY <=1:
                self.won = True
                print('GANEEEEEEEEE')
                self.motor.state = False
                self.game.victories += 1

            if(self.nxtMove == "top"):
                self.y -= 35
                self.pastMove = "top"

            elif (self.nxtMove == "down"):
                self.y += 35
                self.pastMove = "down"

            elif (self.nxtMove == "left"):
                self.x -= 35
                self.pastMove = "left"

            elif (self.nxtMove == "right"):
                self.x += 35
                self.pastMove = "right"
            time.sleep(1)
            self.nxtMove = self.behavior.choosePath(self.possibleMoves,self.pastMove)[0]

        self.game.alive -= 1



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
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_terrain()
        self.possibleMoves = self.camera.findNxtMove()




