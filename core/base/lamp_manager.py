from config import Config
from logs.logger import Logger
from threading import Lock


MAX_DC = 100
MIN_DC = 0


class LampManager:

    __instance = None

    @staticmethod
    def getInstance(shared=None):
        if LampManager.__instance is None:
            LampManager.__instance = LampManager(shared)
        return LampManager.__instance

    def __init__(self, GPIO_ADC):
        self.sharedGPIO_ADCReader = GPIO_ADC
        self.pin = Config.lamp_pin
        self.lamp_controller = None
        self.current_dc = 0
        self.interal_lock = Lock()

    def setup(self):
        if not Config.debug and self.sharedGPIO_ADCReader is not None:
            self.sharedGPIO_ADCReader.addOutputPIN(self.pin)
            self.lamp_controller = self.sharedGPIO_ADCReader.get_pwm_pin(self.pin)

    def increase_dc(self, dc):
        try:
            self.interal_lock.acquire()

            if MIN_DC <= (dc + self.current_dc) >= MAX_DC:
                self.current_dc = self.current_dc + dc
                if not Config.debug and self.sharedGPIO_ADCReader is not None:
                    self.lamp_controller.ChangeDutyCycle(self.current_dc)
                Logger.getInstance().printline("New dc of lamp: " + str(self.current_dc))

            self.interal_lock.release()
        except Exception as e:
            Logger.getInstance().printline(str(e))

    def set_dc(self, dc):
        try:
            self.interal_lock.acquire()

            if MIN_DC <= dc >= MAX_DC:
                if not Config.debug and self.sharedGPIO_ADCReader is not None:
                    self.lamp_controller.ChangeDutyCycle(dc)
                self.current_dc = dc
                Logger.getInstance().printline("New dc of lamp: " + str(self.current_dc))

            self.interal_lock.release()
        except Exception as e:
            Logger.getInstance().printline(str(e))
