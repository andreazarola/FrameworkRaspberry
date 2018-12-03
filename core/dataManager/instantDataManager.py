from core.dataManager.data_manager import DataManager
from threading import Lock
from core.request.db_requestfactory import DBRequestFactory


class InstantDataManager(DataManager):

    def __init__(self):
        super(InstantDataManager, self).__init__()
        self.updateLock = Lock()

    def attach_sensor(self):
        try:
            self.updateLock.acquire()

            self.numSensori += 1

        finally:
            self.updateLock.release()

    def detach_sensor(self):
        try:
            self.updateLock.acquire()

            self.numSensori -= 1

        finally:
            self.updateLock.release()

    def update(self, sensore):
        try:
            self.updateLock.acquire()

            self.addNotitySensor()

            #######################################################
            # Salvataggio del dato sul db
            request = DBRequestFactory().createRequest().initialize()
            request.setTimeStamp(sensore.lastTime)
            request.setTipoDato(sensore.tipoSensore)
            request.setValue(sensore.state)
            request.execute()
            #######################################################

            if self.allDataArrived():
                self.resetNotifySensor()

        finally:
            self.updateLock.release()
