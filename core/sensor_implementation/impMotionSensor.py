#controllare setup e raccolta del dato
from core.sensor_implementation.AbstractImplementation import AbstractImplementation
#import RPi.GPIO as GPIO
import time
import random


class ImpMotionSensor(AbstractImplementation):

    def __init__(self,pin):
        super(ImpMotionSensor, self).__init__(PIN=pin)

    def setup(self):
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.pinSensor,GPIO.IN)
        # tempo dato al sensore per il setup iniziale
        time.sleep(2)

    def get_valore(self):
        #return 0
        return random.randint(0, 1)
        #if GPIO.input(self.pinSensor) == True:
        #    return True
        #return False

    def closeSensor(self):
        time.sleep(2)
        #GPIO.cleanup()