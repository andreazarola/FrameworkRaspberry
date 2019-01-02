from abc import ABC,abstractmethod

class AbstractImplementation(ABC):

    def __init__(self,PIN):
        self.pinSensor=PIN

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def get_valore(self):
        pass
