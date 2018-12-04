from core.dataManager.instantDataManager import InstantDataManager
from core.base.motion_sensor import MotionSensor
from core.base.noise_sensor import NoiseSensor
from core.base.lum_sensor import LuminositySensor
from core.sensor_implementation.impLumSensor import ImpLuminositySensor
from core.sensor_implementation.impNoiseSensor import ImpNoiseSensor
from core.sensor_implementation.impMotionSensor import ImpMotionSensor
from core.pre_elaborazione.elaborate_data import ElaborateData
from core.pre_elaborazione.pre_elaboration_noise import PreElaborationNoise

import schedule
import time


def main():

    #numeroSensori ---> numeroDeiSensori da cui attende dati ogni volta che li deve inviare
    #alla piattaforma di bigData
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

    elaboration_manager.addImplementation(elaboration_noise)



    try:

    #    schedule.every(1).minute.do(s_motion.getData)
    #    schedule.every(1).minute.do(s_noise.getData)
    #    schedule.every(1).minute.do(s_lum.getData)

        schedule.every(1).minute.do(s_motion.getData)
        schedule.every(1).minute.do(s_noise.getData)
        schedule.every(1).minute.do(s_lum.getData)

        schedule.every(1).hour.do(elaboration_manager.update)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        s_motion.closeSensor()
        s_lum.closeSensor()
        s_noise.closeSensor()


if __name__ == "__main__":
    main()
