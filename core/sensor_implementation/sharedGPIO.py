import RPi.GPIO as GPIO
import smbus
from threading import Lock
from logs.logger import Logger
import sys


class SharedGPIO_ADCReader:

    def __init__(self):
        """
        :param busADC: numero del bus per controllare la periferica PCF8591
        """
        GPIO.setmode(GPIO.BCM)
        self.inputPIN = list()
        self.outputPIN = list()
        self.event_detect_pin = list()
        self.channelADCReader = list()
        self.bus = smbus.SMBus(1)
        self.addressADC = None
        """ setup dell'indirizzo di default """
        self.setupADC(0X48)
        self.lockGPIO = Lock()
        self.lockADC = Lock()

    def setupADC(self, address):
        """
        :param address: indirizzo da cui leggere/scrivere verso la periferica PCF8591
        """
        self.addressADC = address

    def addADCChannel(self, chn):
        if chn not in self.channelADCReader:
            self.channelADCReader.append(chn)

    def readADC(self, chn):
        """
        :param chn: canale della periferica PCF8591 dal quale leggere (0..4)
        :return: valore letto dal canale passato come parametro
        """
        try:
            self.lockADC.acquire()
            if self.addressADC is None or chn not in self.channelADCReader:
                return None
            if chn == 0:
                self.bus.write_byte(self.addressADC, 0x40)
            if chn == 1:
                self.bus.write_byte(self.addressADC, 0x41)
            if chn == 2:
                self.bus.write_byte(self.addressADC, 0x42)
            if chn == 3:
                self.bus.write_byte(self.addressADC, 0x43)

            #da controllare se è necessario fare due letture
            self.bus.read_byte(self.addressADC)  # dummy read to start conversion

            return self.bus.read_byte(self.addressADC)
        except Exception as e:
            Logger.getInstance().printline("Address: " + str(self.addressADC))
            Logger.getInstance().printline("Exception in SharedGPIO_ADCReader")
            Logger.getInstance().printline("Chiusura del framework")
            sys.exit(1)
        finally:
            self.lockADC.release()

    def writeADC(self, val):
        """
        :param val: valore da scrivere sul bus della periferica
        """
        try:
            self.lockADC.acquire()
            if self.addressADC is None:
                return None
            temp = val  # move string value to temp
            temp = int(temp)  # change string to integer
            # print temp to see on terminal else comment out
            self.bus.write_byte_data(self.addressADC, 0x40, temp)
        except Exception as e:
            Logger.getInstance().printline("Address: " + str(self.addressADC))
            # gestire eccezione
            Logger.getInstance().printline("Exception in SharedGPIO_ADCReader")
        finally:
            self.lockADC.release()

    def addInputPIN(self, pin):
        """
        :param pin: pin da inizializzare come input
        """
        if pin not in self.inputPIN and pin not in self.outputPIN:
            self.inputPIN.append(pin)
            GPIO.setup(pin, GPIO.IN)

    def addOutputPIN(self, pin):
        """
        :param pin: pin da inizializzare come output
        """
        if pin not in self.inputPIN and pin not in self.outputPIN:
            self.outputPIN.append(pin)
            GPIO.setup(pin, GPIO.OUT)

    def get_pwm_pin(self, pin):
        """
        Dato un pin come parametro restituisce un oggetto PWM su cui cambiare la frequenza
        :param pin: pin da usare per PWM
        :return: oggetto pwm per controllare la frequenza sul pin
        """
        if pin in self.outputPIN:
            pwm = GPIO.PWM(pin, 100)  # Initialize PWM on pwmPin 100Hz frequency
            pwm.start(1)
            return pwm
        return None

    def readGPIO(self, pin):
        """
        :param pin: pin da cui leggere il valore
        :return: valore letto in input dal pin
        """
        try:
            self.lockGPIO.acquire()
            if pin in self.inputPIN:
                val = GPIO.input(pin)
                return val
            return None
        finally:
            self.lockGPIO.release()

    def writeGPIO(self, pin, value):
        """
        :param pin: pin su cui modificare il valore di ouptut
        :param value: nuovo valore da scrivere in output
        :return: True se il pin passato è settato come output, False altrimenti
        """
        try:
            self.lockGPIO.acquire()
            if pin in self.outputPIN:
                GPIO.output(pin, value)
                return True
            return False
        finally:
            self.lockGPIO.release()

    def add_event_detect(self, pin, function):
        if pin not in self.event_detect_pin:
            self.event_detect_pin.append(pin)
            GPIO.add_event_detect(pin, GPIO.RISING, function)

    def clean(self):
        GPIO.cleanup()
        self.inputPIN.clear()
        self.outputPIN.clear()
