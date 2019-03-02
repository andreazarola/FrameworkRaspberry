from sensor_implementation.AbstractImplementation import AbstractImplementation
from config import Config


class ImpRainSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpRainSensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC
        self.trigger_function = None

    def set_trigger_function(self, function):
        self.trigger_function = function

    def setup(self):
        if not Config.debug:
            self.sharedGPIO_ADCReader.addADCChannel(2)
            self.sharedGPIO_ADCReader.addInputPIN(self.PIN)
            self.sharedGPIO_ADCReader.add_event_detect(self.PIN, self.trigger_function)

    def get_valore(self):
        pass