from sensor_implementation.AbstractImplementation import AbstractImplementation
from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader
import random


class ImpNoiseSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpNoiseSensor,self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        self.sharedGPIO_ADCReader.addADCChannel(self.pin)

    def get_valore(self):
        data = random.randint(40, 60)
        #data = self.sharedGPIO_ADCReader.readADC(self.pin)
        return data
