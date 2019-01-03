#controllare setup e raccolta del dato
from sensor_implementation.AbstractImplementation import AbstractImplementation
from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader
import random


class ImpLuminositySensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpLuminositySensor, self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        self.sharedGPIO_ADCReader.addADCChannel(self.PIN)

    def get_valore(self):
        data = random.randint(15, 30)
        data = self.conv(data)
        #data = self.sharedGPIO_ADCReader.readADC(self.PIN)
        return data

    def conv(self, data):
        """
        Commentare la prima linea della funzione per attivare la conversione
        :param data: valore analogico da convertire nell'intervallo (0, 100)
        :return: valore nell'intervallo (0, 100)
        """
        return data
        temp = int((data*100)/250)
        temp = 100 - temp
        return temp
