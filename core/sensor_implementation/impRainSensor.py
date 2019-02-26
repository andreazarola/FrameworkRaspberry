from sensor_implementation.AbstractImplementation import AbstractImplementation
from config import Config
import random


class ImpRainSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpRainSensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        if not Config.debug:
            self.sharedGPIO_ADCReader.addADCChannel(2)
            self.sharedGPIO_ADCReader.addInputPIN(self.PIN)

    def get_valore(self):
        if Config.debug:
            data = random.randint(0, 1)
        else:
            """Potrebbe essere rimossa questa linea"""
            self.sharedGPIO_ADCReader.readADC(2)
            data = int(self.sharedGPIO_ADCReader.readGPIO(self.PIN))
        return data
