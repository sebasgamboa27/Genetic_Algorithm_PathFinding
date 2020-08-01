class Battery:
    def __init__(self,batteryLvl):
        self.batteryCapacity = 0
        self.batteryLvl = batteryLvl
        if(batteryLvl == 1):
            self.batteryCapacity = 100
        if (batteryLvl == 2):
            self.batteryCapacity = 150
        if (batteryLvl == 3):
            self.batteryCapacity = 175
        self.battery = self.batteryCapacity
        self.batteryPercentage = (self.battery/self.batteryCapacity)*100

    def consumeBattery(self,amount):
        self.battery -= amount
        self.updatePercentage()

    def restoreBattery(self):
        self.battery = self.batteryCapacity
        self.updatePercentage()

    def consumeAllBattery(self):
        self.battery -= self.battery
        self.updatePercentage()

    def updatePercentage(self):
        self.batteryPercentage = (self.battery / self.batteryCapacity) * 100