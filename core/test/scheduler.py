from apscheduler.schedulers.background import BackgroundScheduler
import time


class Scheduler:

    _instance = None

    @staticmethod
    def get_instance():
        if Scheduler._instance is None:
            Scheduler._instance = Scheduler()
        return Scheduler._instance

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.job_list = list()
        self.misfire_grace_time = 10

    def edit_job(self, job_id, second, minute, hour):
        if job_id in self.job_list:
            print(job_id + "modificato")
            self.scheduler.reschedule_job(job_id, trigger='cron', second=second,
                                          minute=minute, hour=hour)
            return True
        return False

    def add_job(self, function=None, second='*', minute='*', hour='*', job_id=''):
        self.scheduler.add_job(function, 'cron', second=second, minute=minute, hour=hour, id=job_id,
                               misfire_grace_time=self.misfire_grace_time)
        self.job_list.append(job_id)

    def initialize(self):
        self.scheduler.start()

    def run(self):
        while True:
            time.sleep(1)