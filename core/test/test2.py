from core.dataManager.instantDataManager import InstantDataManager
from core.base.motion_sensor import MotionSensor
from core.base.noise_sensor import NoiseSensor
from core.base.lum_sensor import LuminositySensor
from core.sensor_implementation.impLumSensor import ImpLuminositySensor
from core.sensor_implementation.impNoiseSensor import ImpNoiseSensor
from core.sensor_implementation.impMotionSensor import ImpMotionSensor
from core.pre_elaborazione.elaborate_data import ElaborateData
from core.pre_elaborazione.pre_elaboration_noise import PreElaborationNoise
from core.pre_elaborazione.pre_elaboration_motion import PreElaborationMotion
from core.pre_elaborazione.pre_elaboration_lum import PreElaborationLum

from apscheduler.schedulers.background import BackgroundScheduler
import time


def main():

    data_manager = InstantDataManager()
    imp_motion = ImpMotionSensor(pin=2)
    imp_noise = ImpNoiseSensor(pin=3)
    imp_lum = ImpLuminositySensor(pin=4)

    s_motion = MotionSensor(imp_motion, data_manager)
    s_motion.setup()
    s_noise = NoiseSensor(imp_noise, data_manager)
    s_noise.setup()
    s_lum = LuminositySensor(imp_lum, data_manager)
    s_lum.setup()

    elaboration_manager = ElaborateData()
    elaboration_noise = PreElaborationNoise()
    elaboration_motion = PreElaborationMotion()
    elaboration_lum = PreElaborationLum()

    elaboration_manager.addImplementation(elaboration_noise)
    elaboration_manager.addImplementation(elaboration_motion)
    elaboration_manager.addImplementation(elaboration_lum)

    scheduler = BackgroundScheduler()

    try:

        scheduler.add_job(s_motion.getData, 'cron', second=0)
        scheduler.add_job(s_noise.getData, 'cron', second=0)
        scheduler.add_job(s_lum.getData, 'cron', second=0)

        scheduler.add_job(elaboration_manager.update, 'cron', minute=0, second=0)

        scheduler.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        s_motion.closeSensor()
        s_lum.closeSensor()
        s_noise.closeSensor()
        scheduler.shutdown()


if __name__ == "__main__":
    main()
