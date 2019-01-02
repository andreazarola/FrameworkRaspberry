from test.launcher import Launcher
from local_db.init_db import init_db
from base.motion_sensor import MotionSensor
from base.noise_sensor import NoiseSensor
from base.lum_sensor import LuminositySensor
from sensor_implementation.impLumSensor import ImpLuminositySensor
from sensor_implementation.impNoiseSensor import ImpNoiseSensor
from sensor_implementation.impMotionSensor import ImpMotionSensor
from pre_elaborazione.pre_elaboration_noise import PreElaborationNoise
from pre_elaborazione.pre_elaboration_motion import PreElaborationMotion
from pre_elaborazione.pre_elaboration_lum import PreElaborationLum
import sys


def main():
    init_db(sys.path[0] + "/local_db/")
    launcher = Launcher()
    launcher.aggiungiSensore(MotionSensor(ImpMotionSensor(pin=2), launcher.dataManager))
    launcher.aggiungiSensore(LuminositySensor(ImpLuminositySensor(pin=3), launcher.dataManager))
    launcher.aggiungiSensore(NoiseSensor(ImpNoiseSensor(pin=4), launcher.dataManager))

    launcher.aggiungiElaborazione(PreElaborationMotion())
    launcher.aggiungiElaborazione(PreElaborationLum())
    launcher.aggiungiElaborazione(PreElaborationNoise())

    launcher.run()


if __name__ == "__main__":
    main()
