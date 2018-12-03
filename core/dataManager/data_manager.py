from abc import ABC,abstractmethod


class DataManager(ABC):

    def __init__(self):
        self.numSensori = 0
        self.countSensori = 0

    @abstractmethod
    def attach_sensor(self):
        pass

    @abstractmethod
    def detach_sensor(self):
        pass

    @abstractmethod
    def update(self,sensore):
       pass

    def addNotitySensor(self):
        self.countSensori += 1

    def resetNotifySensor(self):
        self.countSensori = 0

    def allDataArrived(self):
        return self.countSensori == self.numSensori