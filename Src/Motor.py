from Battery import *

class Motor:
    def __init__(self, motorLvl,batteryLvl):
        self.battery = Battery(batteryLvl)
        self.type = motorLvl
        self.state = True

    def checkState(self):
        if(self.battery.battery <= 0):
            self.state = False
            print('Motor apagado')
        else:
            print(self.battery.batteryPercentage,"%")

        return self.state

    def shutDown(self):
        self.battery.consumeAllBattery()
        self.checkState()

    def move(self,terrain):
        if (terrain.type == 1):
            self.battery.consumeBattery(1)

        elif (terrain.type == 2):
            self.battery.consumeBattery(2)

        elif (terrain.type == 3):
            self.battery.consumeBattery(3)

        self.checkState()



