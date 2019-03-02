from sensor_implementation.AbstractImplementation import AbstractImplementation
from logs.logger import Logger
from config import Config
import time


class ImpMotionSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpMotionSensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC
        self.trigger_function = None

    def set_trigger_function(self, function):
        self.trigger_function = function

    def setup(self):
        """il sensore di movimento ha bisogno di circa un minuto per il setup iniziale"""
        if not Config.debug:
            self.sharedGPIO_ADCReader.addInputPIN(self.PIN)
            Logger.getInstance().printline("Setup iniziale motion sensor in corso")
            time.sleep(60)
            Logger.getInstance().printline("Setup iniziale motion sensor finito")
            self.sharedGPIO_ADCReader.add_event_detect(self.PIN, self.trigger_function)

    def get_valore(self):
        pass