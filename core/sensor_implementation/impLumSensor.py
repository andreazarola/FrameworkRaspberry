#controllare setup e raccolta del dato
from core.sensor_implementation.AbstractImplementation import AbstractImplementation
import time
import random


class ImpLuminositySensor(AbstractImplementation):

    def __init__(self,pin):
        super(ImpLuminositySensor, self).__init__(PIN=pin)

    def setup(self):
        time.sleep(2)
        pass

    def get_valore(self):
        #return 21
        return random.randint(15, 30)
        #pass

    def closeSensor(self):
        time.sleep(1)
        #pass
