from Battery import *

class Motor:
    def __init__(self,robot, motorLvl,batteryLvl):
        self.battery = Battery(batteryLvl)
        self.type = motorLvl
        self.state = True
        self.robot = robot

    def checkState(self):
        if(self.battery.battery <= 0):
            self.state = False
            print('Motor apagado')
            self.robot.x = 1000
            self.robot.y = 1000

        else:
            print("Batería del robot: ",self.robot.id,self.battery.battery,"%")

        return self.state

    def shutDown(self):
        self.battery.consumeAllBattery()
        self.checkState()

    def consumeBattery(self,cant):
        self.battery.consumeBattery(cant)
        self.checkState()

    def move(self,terrain):
        if (terrain.type == 1):
            self.battery.consumeBattery(1)

        elif (terrain.type == 2):
            self.battery.consumeBattery(2)

        elif (terrain.type == 3):
            self.battery.consumeBattery(3)

        self.checkState()



