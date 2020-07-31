class Camera:
    def __init__(self, logicMaze,pos,lvl):
        self.x = pos[0]
        self.y = pos[1]
        self.logicMaze = logicMaze
        self.radius = lvl


    def findNxtMove(self):
        possibleMoves = []

        try:
            if self.logicMaze[self.y][self.x+1] == 0:
                possibleMoves += ['right']
        except:
            print("Se acabo el mapa")

        try:
            if self.logicMaze[self.y][self.x-1] == 0:
                possibleMoves += ['left']
        except:
            print("Se acabo el mapa")

        try:
            if self.logicMaze[self.y+1][self.x] == 0:
                possibleMoves += ['down']
        except:
            print("Se acabo el mapa")

        try:
            if self.logicMaze[self.y-1][self.x] == 0:
                possibleMoves += ['top']
        except:
            print("Se acabo el mapa")

        return possibleMoves

    def updateLocation(self,x,y):
        self.x = x
        self.y = y




