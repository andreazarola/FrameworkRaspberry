from dataManager.instantDataManager import InstantDataManager
from pre_elaborazione.elaborate_data import ElaborateData
from apscheduler.schedulers.background import BackgroundScheduler
import time


class Launcher:

    def __init__(self):
        self.dataManager = InstantDataManager()
        self.elaborateManager = ElaborateData()
        self.sensors = list()
        self.scheduler = BackgroundScheduler()
        self.triggerSecond = 0
        self.triggerMinute = 0

    def aggiungiSensore(self, sensore):
        self.sensors.append(sensore)

    def aggiungiElaborazione(self, elaboration):
        self.elaborateManager.addImplementation(elaboration)

    def run(self):
        if not self.sensors:
            raise Exception("Aggiungere almeno un sensore al launcher")
            return

        for s in self.sensors:
            s.setup()

        try:
            for s in self.sensors:
                self.scheduler.add_job(s.getData, 'cron', second=self.triggerSecond)

            self.scheduler.add_job(self.elaborateManager.update, 'cron', minute=self.triggerMinute, second=self.triggerSecond)

            self.scheduler.start()

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            for s in self.sensors:
                s.closeSensor()
