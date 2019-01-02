#controllare setup e raccolta del dato
from sensor_implementation.AbstractImplementation import AbstractImplementation
from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader
import random


class ImpLuminositySensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpLuminositySensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        self.sharedGPIO_ADCReader.addADCChannel(self.pin)

    def get_valore(self):
        data = random.randint(15, 30)
        #data = self.sharedGPIO_ADCReader.readADC(self.pin)
        return data
