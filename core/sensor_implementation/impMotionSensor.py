from sensor_implementation.AbstractImplementation import AbstractImplementation
from logs.logger import Logger
from config import Config
import random
import time


class ImpMotionSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpMotionSensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        """il sensore di movimento ha bisogno di circa un minuto per il setup iniziale"""
        if not Config.debug:
            self.sharedGPIO_ADCReader.addInputPIN(self.PIN)
            Logger.getInstance().printline("Setup iniziale motion sensor in corso")
            time.sleep(60)
            Logger.getInstance().printline("Setup iniziale motion sensor finito")

    def get_valore(self):
        if Config.debug:
            data = random.randint(0, 1)
        else:
            data = int(self.sharedGPIO_ADCReader.readGPIO(self.PIN))
        return data
