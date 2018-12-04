from abc import ABC, abstractmethod


class DataManager(ABC):

    def __init__(self):
        self.count_sensori = 0
        self.sensor_list = list()

    @abstractmethod
    def attach_sensor(self, tipo_sensore):
        pass

    @abstractmethod
    def detach_sensor(self, tipo_sensore):
        pass

    @abstractmethod
    def update(self, sensore):
       pass

    def addNotitySensor(self):
        self.count_sensori += 1

    def resetNotifySensor(self):
        self.count_sensori = 0

    def allDataArrived(self):
        return self.countSensori == len(self.sensor_list)
