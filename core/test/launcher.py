from dataManager.instantDataManager import InstantDataManager
from pre_elaborazione.elaborate_data import ElaborateData
from apscheduler.schedulers.background import BackgroundScheduler
from base.lamp_manager import LampManager
from alert_listener.listener import AlertListener
from alert_listener.alert_queue import AlertQueue
from alert_listener.alert_executor import AlertExecutor
from logs.logger import Logger
from local_db.clean_old_data import clean_old_data
import time


class Launcher:

    def __init__(self):
        self.dataManager = InstantDataManager()
        self.elaborateManager = ElaborateData()
        self.sensors = list()
        self.scheduler = BackgroundScheduler()
        self.triggerSecond = 0
        self.triggerMinute = 0
        self.sharedGPIO_ADC = None
        self.lamp_manager = None
        self.alert_listener = AlertListener()
        self.alert_queue = AlertQueue.get_instance()
        self.alert_executor = None

    def setGPIO_ADC(self, GPIO_ADC):
        self.sharedGPIO_ADC = GPIO_ADC
        self.lamp_manager = LampManager.getInstance(self.sharedGPIO_ADC)

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

        self.alert_executor = AlertExecutor(self.alert_queue, self.lamp_manager)

        #self.lamp_manager.setup()
        self.alert_listener.start()
        self.alert_executor.start()

        try:
            for s in self.sensors:
                self.scheduler.add_job(s.getData, 'cron', second=self.triggerSecond)

            self.scheduler.add_job(self.elaborateManager.update, 'cron', minute=self.triggerMinute, second=self.triggerSecond)
            self.scheduler.add_job(clean_old_data, 'cron', minute=0, second=0, hour=23)
            self.scheduler.start()

            Logger.getInstance().printline("Started")

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            for s in self.sensors:
                s.closeSensor()
            if self.sharedGPIO_ADC is not None:
                self.sharedGPIO_ADC.clean()
