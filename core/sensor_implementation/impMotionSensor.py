#controllare setup e raccolta del dato
from sensor_implementation.AbstractImplementation import AbstractImplementation
from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader
import random


class ImpMotionSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpMotionSensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        self.sharedGPIO_ADCReader.addInputPIN(self.PIN)

    def get_valore(self):
        data = random.randint(0, 1)
        #data = int(self.sharedGPIO_ADCReader.readGPIO(self.PIN))
        return data
