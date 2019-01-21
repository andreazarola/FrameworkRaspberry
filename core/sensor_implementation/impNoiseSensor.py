from sensor_implementation.AbstractImplementation import AbstractImplementation
from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader
import random


class ImpNoiseSensor(AbstractImplementation):

    def __init__(self, pin, GPIO_ADC):
        super(ImpNoiseSensor,self).__init__(PIN=pin)
        self.sharedGPIO_ADCReader = GPIO_ADC

    def setup(self):
        self.sharedGPIO_ADCReader.addADCChannel(self.PIN)

    def get_valore(self):
        data = random.randint(40, 60)
        #data = self.sharedGPIO_ADCReader.readADC(self.PIN)
        data = self.conv(data)
        return data

    def conv(self, data):
        """
        Commentare la prima linea della funzione per attivare la conversione
        :param data: valore analogico da convertire nell'intervallo (0, 100)
        :return: valore nell'intervallo (0, 100)
        """
        return data
        temp = int(((data-60)*100)/160)
        temp = 100 - temp
        return temp