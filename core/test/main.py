from core.dataManager.instantDataManager import InstantDataManager
from core.base.motion_sensor import MotionSensor
from core.base.noise_sensor import NoiseSensor
from core.base.lum_sensor import LuminositySensor
from core.sensor_implementation.impLumSensor import ImpLuminositySensor
from core.sensor_implementation.impNoiseSensor import ImpNoiseSensor
from core.sensor_implementation.impMotionSensor import ImpMotionSensor
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

    try:

        schedule.every(1).minute.do(s_motion.getData)
        schedule.every(1).minute.do(s_noise.getData)
        schedule.every(1).minute.do(s_lum.getData)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        s_motion.closeSensor()


if __name__ == "__main__":
    main()