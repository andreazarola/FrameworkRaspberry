from threading import Thread
import time
from config import Config

colors = [100, 0]


class AlarmLed(Thread):

    def __init__(self, sharedGPIO_ADCReader):
        self.sharedGPIO_ADCReader = sharedGPIO_ADCReader
        self.pin = 23
        super(AlarmLed, self).__init__()

    def run(self):
        if not Config.debug:
            added = self.sharedGPIO_ADCReader.addOutputPIN(self.pin)
            if added is True:
                self.sharedGPIO_ADCReader.writeGPIO(self.pin, 0)
                controller = self.sharedGPIO_ADCReader.get_pwm_pin(self.pin)
                controller.start(0)
                i = 0
                while i < 3:
                    for col in colors:
                        controller.ChangeDutyCycle(col)
                        time.sleep(1)
                    i += 1
                controller.stop()
                self.sharedGPIO_ADCReader.writeGPIO(self.pin, 0)
                self.sharedGPIO_ADCReader.removeOutputPIN(self.pin)
