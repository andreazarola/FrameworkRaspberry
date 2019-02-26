from dataManager.instantDataManager import InstantDataManager
from pre_elaborazione.elaborate_data import ElaborateData
from base.lamp_manager import LampManager
from alert_listener.listener import AlertListener
from alert_listener.alert_queue import AlertQueue
from alert_listener.alert_executor import AlertExecutor
from logs.logger import Logger
from local_db.clean_old_data import clean_old_data
from configuration.configuration_trigger import ConfigurationTrigger
from test.scheduler import Scheduler
import time


class Launcher:

    def __init__(self):
        self.dataManager = InstantDataManager()
        self.elaborateManager = ElaborateData()
        self.sensors = list()
        self.scheduler = Scheduler.get_instance()
        self.triggerSecond = 0
        self.triggerMinute = 0
        self.max_late_allowed = 10
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

        self.alert_listener.start()
        self.alert_executor.start()

        try:
            conf_trigger = ConfigurationTrigger.get_instance()

            for s in self.sensors:
                trigger = conf_trigger.get_trigger(s.tipoSensore)
                self.scheduler.add_job(function=s.getData, second=trigger.get_second(), minute=trigger.get_minute(),
                                       hour=trigger.get_hour(), job_id=s.tipoSensore)

            self.scheduler.add_job(function=self.elaborateManager.update, minute=self.triggerMinute,
                                   second=self.triggerSecond, job_id="elaborate_manager")
            self.scheduler.add_job(function=clean_old_data, minute='0', second='0', hour='23',
                                   job_id="clean_old_data")

            self.scheduler.initialize()
            Logger.getInstance().printline("Started")
            self.scheduler.run()

        except KeyboardInterrupt:
            for s in self.sensors:
                s.closeSensor()
            if self.sharedGPIO_ADC is not None:
                self.sharedGPIO_ADC.clean()
