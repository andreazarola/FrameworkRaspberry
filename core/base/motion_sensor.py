from base.sensor import Sensore
from datetime import datetime
from logs.logger import Logger


class MotionSensor(Sensore):

    def __init__(self, implementation, observer):
        super(MotionSensor, self).__init__(implementation, observer, "Presenza")
        self.implementation.set_trigger_function(self.getData)

    def getData(self, pin):
        """
        Viene rimimplementato il metodo della classe padre
        :return:
        """
        self.state = 1
        self.lastTime = datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")
        Logger.getInstance().printline("Tempo cattura del dato di " + self.tipoSensore + ": " + self.lastTime +
                                       ",\t valore:" + str(self.state))

        self.notify()
