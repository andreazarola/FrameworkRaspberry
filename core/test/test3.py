from core.test.launcher import Launcher
from core.local_db.init_db import init_db
from core.base.motion_sensor import MotionSensor
from core.base.noise_sensor import NoiseSensor
from core.base.lum_sensor import LuminositySensor
from core.sensor_implementation.impLumSensor import ImpLuminositySensor
from core.sensor_implementation.impNoiseSensor import ImpNoiseSensor
from core.sensor_implementation.impMotionSensor import ImpMotionSensor
from core.pre_elaborazione.pre_elaboration_noise import PreElaborationNoise
from core.pre_elaborazione.pre_elaboration_motion import PreElaborationMotion
from core.pre_elaborazione.pre_elaboration_lum import PreElaborationLum


def main():
    init_db()
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
