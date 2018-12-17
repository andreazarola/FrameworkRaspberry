#controllare setup e raccolta del dato
from sensor_implementation.AbstractImplementation import AbstractImplementation
#import PCF8591 as ADC
#import RPi.GPIO as GPIO
import time
import random

class ImpNoiseSensor(AbstractImplementation):

    def __init__(self, pin):
        super(ImpNoiseSensor,self).__init__(PIN=pin)

    def setup(self):
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.pinSensor,GPIO.IN)
        # tempo dato al sensore per il setup iniziale
        time.sleep(2)

    def get_valore(self):
        #data = 51
        data = random.randint(40, 60)
        #data = ADC.read(0)
        return data

    def closeSensor(self):
        time.sleep(1)
        #GPIO.cleanup()