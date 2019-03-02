from base.sensor import Sensore
from logs.logger import Logger
from datetime import datetime


class RainSensor(Sensore):

    def __init__(self, implementation, observer):
        super(RainSensor, self).__init__(implementation, observer, "Pioggia")
        self.implementation.set_trigger_function(self.getData)

    def getData(self, pin):
        """
        Viene rimplementato il metodo della classe padre
        :return:
        """
        self.state = 1
        self.lastTime = datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")
        Logger.getInstance().printline("Tempo cattura del dato di " + self.tipoSensore + ": " + self.lastTime +
                                       ",\t valore:" + str(self.state))

        self.notify()
