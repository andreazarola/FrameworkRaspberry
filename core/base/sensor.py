from abc import ABC
from datetime import datetime
from logs.logger import Logger

class Sensore(ABC):

    def __init__(self, implementation, observer, tipoSensore):
        self.implementation = implementation
        self.observer = observer
        self.tipoSensore = tipoSensore
        self.state = None
        self.lastTime = None

    def setup(self):
        self.implementation.setup()
        """
        Quando collego un sensore al dataManager passo anche il tipo di sensore in modo
        che il dataManager sappia quale sensore è stato collegato
        """
        self.observer.attach_sensor(self.tipoSensore)


    def getData(self):
        """
        Metodo che viene schedulata
        :return:
        """
        self.state = self.implementation.get_valore()
        self.lastTime = datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")

        Logger.getInstance().printline("Tempo cattura del dato di " + self.tipoSensore + ": " + self.lastTime +
                                       ",\t valore:" + str(self.state))

        self.notify()

    def notify(self):
        self.observer.update(self)

    def closeSensor(self):
        self.observer.detach_sensor(self.tipoSensore)
