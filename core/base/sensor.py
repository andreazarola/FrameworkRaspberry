from abc import ABC
from datetime import datetime

class Sensore(ABC):

    def __init__(self, implementation, observer, tipoSensore):
        self.implementation = implementation
        self.observer = observer
        self.tipoSensore = tipoSensore
        self.state = None
        self.lastTime = None

    def setup(self):
        self.implementation.setup()
        self.observer.attach_sensor()

    #funzione da schedulare
    def getData(self):
        self.state = self.implementation.get_valore()
        self.lastTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        ######################################
        print ("Tempo cattura del dato di " + self.tipoSensore)
        print (self.lastTime)
        ######################################
        self.notify()

    def notify(self):
        self.observer.update(self)

    def closeSensor(self):
        self.observer.detach_sensor()
        self.implementation.closeSensor()