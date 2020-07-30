import random

class DNA(object):
    def __init__(self, genes=None):
        self.array = []
        if genes:
            self.array = genes
        else:
            for i in range(4):

                right = random.randint(0,100)
                top = random.randint(0,100 - right)
                left = random.randint(0,100 - right - top)
                down = 100- right - top - left
                chainNode = [right,top,left,down]
                self.array.append(chainNode)

    def crossOver(self, partner):

        newGenes = []
        middle = math.floor(random.randrange(len(self.array)))

        for i in range(len(self.array)):
            if i < middle:
                newGenes.append(partner.array[i])
            else:
                newGenes.append(self.array[i])

        return DNA(newGenes)

    def choosePath(self,available,currentState):

        choices = ['right','top','left','down']
        choiceMade = None

        while choiceMade is None:

            if currentState == 'right':
                direction = random.choices(choices,
                               weights=(self.array[0][0], self.array[0][1],
                                        self.array[0][2], self.array[0][3]), k=1)

                if direction in available:
                    choiceMade = direction

            elif currentState == 'top':
                direction = random.choices(choices,
                               weights=(self.array[1][0], self.array[1][1],
                                        self.array[1][2], self.array[1][3]), k=1)

                if direction in available:
                    choiceMade = direction

            elif currentState == 'left':
                direction = random.choices(choices,
                                           weights=(self.array[2][0], self.array[2][1],
                                                    self.array[2][2], self.array[2][3]), k=1)

                if direction in available:
                    choiceMade = direction

            else:
                direction = random.choices(choices,
                                           weights=(self.array[3][0], self.array[3][1],
                                                    self.array[3][2], self.array[3][3]), k=1)

                if direction in available:
                    choiceMade = direction

