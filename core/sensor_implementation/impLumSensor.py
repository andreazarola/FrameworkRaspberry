from sensor_implementation.AbstractImplementation import AbstractImplementation
from config import Config
import random


class ImpLuminositySensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpLuminositySensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        if not Config.debug:
            self.sharedGPIO_ADCReader.addADCChannel(self.PIN)

    def get_valore(self):
        if Config.debug:
            data = random.randint(50, 100)
        else:
            data = self.sharedGPIO_ADCReader.readADC(self.PIN)
        data = self.conv(data)
        return data

    def conv(self, data):
        """
        Commentare la prima linea della funzione per attivare la conversione
        :param data: valore analogico da convertire nell'intervallo (0, 100)
        :return: valore nell'intervallo (0, 100)
        """
        if Config.convertData:
            return data
        else:
            temp = int((data*100)/250)
            temp = 100 - temp
            return temp
