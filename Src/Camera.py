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
            None
        try:
            if self.logicMaze[self.y][self.x-1] == 0:
                possibleMoves += ['left']
        except:
            None

        try:
            if self.logicMaze[self.y+1][self.x] == 0:
                possibleMoves += ['down']
        except:
            None

        try:
            if self.logicMaze[self.y-1][self.x] == 0:
                possibleMoves += ['top']
        except:
            None

        return possibleMoves

    def updateLocation(self,x,y):
        self.x = x
        self.y = y




