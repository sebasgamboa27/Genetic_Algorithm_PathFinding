import pygame as pg
import numpy as np
import sys
import random
import time
from os import path
from settings import *
from Terrain import *
from Robot import *
import math



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
        self.oldGen = []
        self.deadGen = False
        self.genSize = genSize
        self.finish = pg.math.Vector2()
        self.finish.xy = 18,1
        self.genePool = []
        self.genNum = 1
        self.finished = False
        self.logicMaze = np.zeros((20, 20), int)
        self.lowestTime = 0
        self.victories = 0
        self.best = None
        self.bestIndex = 0
        self.alive = genSize
        self.frames = 0
        self.avFitness = 0
        pg.font.init()
        self.font = pg.font.Font('MinecraftItalic-R8Mo.otf', 30)

    def Distance(self, x1, x2, y1, y2):
        dis = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return (30 - dis) / 30

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
        self.logicMaze = np.zeros((20,20),int)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    self.setTerrain(col,row)
                if tile == '1':
                    if(col < 20 and row < 20):
                        self.logicMaze[row][col] = 1
                    Wall(self, col, row)
                if tile == 'P':
                    Terrain(self,col,row,1)
                    for i in range(self.genSize):
                        newPlayer = Player(self, col, row,i)
                        self.generation.append(newPlayer)
                        if i == 1:
                            self.best = newPlayer
                if tile == 'F':
                    print('Finish Line')
        for i in range(self.genSize):
            self.generation[i].configure(self.logicMaze)

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

    def checkGen(self):
        for robot in self.generation:
            if robot.motor.state:
                return False
        return True

    def moveGen(self):
        for robot in self.generation:
            self.oldGen.append(robot)
        self.generation.clear()



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if(self.checkGen()):
                self.moveGen()
                self.deadGen = True

            if self.deadGen:
                self.deadGen = False
                self.clearOldGenOnScreen()
                print("GENARACION CREADA")
                #AQUI VA SU FUNCION DE INSERTAR LA NUEVA GEN EN self.generation
                self.FinishGeneration()
                #self.createGen()
                self.clearOldGen()
                self.alive = self.genSize
                self.victories = 0
                print('Generacion: ',self.genNum)


            self.events()
            self.update()
            self.draw()

    def createGen(self):
        #Cambie este codigo, pero tiene que hacer algo similar, un for para colocarlos otro para iniciarlos
        for i in range(self.genSize):
            self.generation.append(Player(self, 1, 19, i))

        for i in range(self.genSize):
            self.generation[i].configure(self.logicMaze)

    def clearOldGenOnScreen(self):
        for robot in self.oldGen:
            robot.x = robot.y = 1000

    def clearOldGen(self):
        for bot in self.oldGen:
            bot.kill()
        self.oldGen.clear()

    def FinishGeneration(self):

        tempAvgFitness = 0
        tempSuccessCount = 0
        self.genePool.clear()
        maxFit = 0
        lowestIndex = 0
        successCount = 0
        avgFitnessSum = 0
        maxFitIndex = 0

        for box in self.oldGen:
            box.CalculateFitness()
            avgFitnessSum += box.fitness
            if box.fitness >= 1.0 or box.won:
                successCount += 1
            if box.fitness > maxFit:
                maxFit = box.fitness
                maxFitIndex = self.oldGen.index(box)
        successCountD = successCount - tempSuccessCount
        avgFitness = avgFitnessSum / len(self.oldGen)
        avgFitnessD = avgFitness - tempAvgFitness
        self.avFitness = avgFitnessD


        for i, box in enumerate(self.oldGen):
            if box.won:
                self.victories+=1
                if box.motor.battery.battery > self.lowestTime:
                    lowestIndex = i
                    self.lowestTime = box.motor.battery.battery

        for i, box in enumerate(self.oldGen):

            n = int((box.fitness ** 2) * 100)

            if i == maxFitIndex:
                print(box.fitness)
                self.bestIndex = maxFitIndex
                self.best = self.oldGen[maxFitIndex]
                if successCount < 2:
                    n = int((box.fitness ** 2) * 150)

            if i == lowestIndex and successCount > 1:
                n = int((box.fitness ** 2) * 500)
            for j in range(n):
                self.genePool.append(self.oldGen[i])

        if successCount >= 100:
            print('ganaron todos')

        else:
            for i, box in enumerate(self.oldGen):
                randomIndex = random.randint(0, len(self.genePool) - 1)
                parentA = self.genePool[randomIndex].behavior
                parentACOMPLETE = self.genePool[randomIndex]
                randomIndex = random.randint(0, len(self.genePool) - 1)
                parentB = self.genePool[randomIndex].behavior
                parentBCOMPLETE = self.genePool[randomIndex]
                child = parentA.crossOver(parentB)
                player = Player(self, 1, 19, i, child.array)
                player.Parents[0] = parentACOMPLETE
                player.Parents[1] = parentBCOMPLETE
                self.generation.append(player)

            for i in range(self.genSize):
                self.generation[i].configure(self.logicMaze)
            self.genNum += 1


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
        self.screen.blit(TITLEIMAGE, (750, 20))
        self.screen.blit(GENERACIONIMAGE, (720, 100))
        self.screen.blit(ROBOTSIMAGE, (720, 150))
        self.screen.blit(FINISHEDIMAGE, (720, 200))
        self.screen.blit(AVERAGE, (720, 250))
        self.screen.blit(LOWEST, (720, 300))
        self.screen.blit(BEST, (720, 350))

        self.screen.blit(self.font.render(str(self.genNum), False, (254, 0, 0)),(960,95))
        self.screen.blit(self.font.render(str(self.alive), False, (254, 0, 0)), (860, 145))
        self.screen.blit(self.font.render(str(self.victories), False, (254, 0, 0)), (900, 195))
        self.screen.blit(self.font.render(str(round(self.avFitness,3)), False, (254, 0, 0)), (1000, 245))
        self.screen.blit(self.font.render(str(self.lowestTime)+'%', False, (254, 0, 0)), (960, 295))
        if self.best is not None:
            delimiter = ''
            delimiter2 = ''
            if self.genNum > 2:
                final_strA = 'A: ' + 'right('+ str(self.best.Parents[0].behavior.array[0]).strip('[]')+') '+\
                             'top('+str(self.best.Parents[0].behavior.array[1]).strip('[]')+')'

                final_strA2 = 'left('+str(self.best.Parents[0].behavior.array[2]).strip('[]')+') '+\
                             'down('+str(self.best.Parents[0].behavior.array[3]).strip('[]')+')'


                final_strB = 'B: ' + 'right('+ str(self.best.Parents[1].behavior.array[0]).strip('[]')+') '+\
                             'top('+str(self.best.Parents[1].behavior.array[1]).strip('[]')+')'

                final_strB2 = 'left(' + str(self.best.Parents[1].behavior.array[2]).strip('[]') + ') ' +\
                              'down(' + str(self.best.Parents[1].behavior.array[3]).strip('[]')+')'
            else:
                final_strA = 'None'
                final_strB = 'None'
                final_strA2 = 'None'
                final_strB2 = 'None'

            finalstrC = 'Motor: ' + str(self.best.motor.type)
            finalstrD = 'Bateria: ' + str(self.best.motor.battery.batteryLvl)
            finalstrE = 'Camara: ' + str(self.best.cameraLvl)
            self.screen.blit(self.font.render(str(finalstrC), False, (254, 0, 0)), (720, 595))
            self.screen.blit(self.font.render(str(finalstrD), False, (254, 0, 0)), (720, 645))
            self.screen.blit(self.font.render(str(finalstrE), False, (254, 0, 0)), (720, 695))
            self.screen.blit(self.font.render(str(final_strA), False, (254, 0, 0)), (720, 395))
            self.screen.blit(self.font.render(str(final_strA2), False, (254, 0, 0)), (720, 445))
            self.screen.blit(self.font.render(str(final_strB), False, (254, 0, 0)), (720, 495))
            self.screen.blit(self.font.render(str(final_strB2), False, (254, 0, 0)), (720, 545))

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
