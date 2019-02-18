from test.launcher import Launcher
from local_db.init_db import init_db
from base.motion_sensor import MotionSensor
from base.noise_sensor import NoiseSensor
from base.lum_sensor import LuminositySensor
from base.led_sensor import LedSensor
from base.lamp_manager import LampManager
from sensor_implementation.impLumSensor import ImpLuminositySensor
from sensor_implementation.impNoiseSensor import ImpNoiseSensor
from sensor_implementation.impMotionSensor import ImpMotionSensor
from pre_elaborazione.pre_elaboration_noise import PreElaborationNoise
from pre_elaborazione.pre_elaboration_motion import PreElaborationMotion
from pre_elaborazione.pre_elaboration_lum import PreElaborationLum
from logs.logger import Logger
from configuration.configuration_handler import ConfigurationHandler
from config_server import ConfigurationServer
from config import Config
import sys
import atexit


def commit_config():
    ConfigurationHandler.get_instance().save_config()


def load_configs():
    path = sys.path[0]
    config_file = path + '/configuration_file'
    file = open(config_file, 'r')

    conf_handler = ConfigurationHandler.get_instance(config_file)

    for line in file.readlines()[1:]:
        conf_handler.add_param(line.rstrip())


def main():

    from sensor_implementation.sharedGPIO import SharedGPIO_ADCReader

    path = sys.path[0]
    option = sys.argv[1] if len(sys.argv) > 1 else None
    if option == "-log":
        log = Logger.getInstance()
        log.init_logger(path)
    init_db(path + "/local_db/")
    launcher = Launcher()
    shared = SharedGPIO_ADCReader()
    launcher.setGPIO_ADC(shared)
    launcher.aggiungiSensore(MotionSensor(ImpMotionSensor(pin=17, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(LuminositySensor(ImpLuminositySensor(pin=1, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(NoiseSensor(ImpNoiseSensor(pin=0, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(LedSensor(LampManager.getInstance(shared), launcher.dataManager))

    launcher.aggiungiElaborazione(PreElaborationMotion())
    launcher.aggiungiElaborazione(PreElaborationLum())
    launcher.aggiungiElaborazione(PreElaborationNoise())

    launcher.run()


def main_debug():
    path = sys.path[0]
    option = sys.argv[1] if len(sys.argv) > 1 else None
    if option == "-log":
        log = Logger.getInstance()
        log.init_logger(path)
    init_db(path + "/local_db/")
    launcher = Launcher()
    shared = None
    launcher.setGPIO_ADC(shared)
    launcher.aggiungiSensore(MotionSensor(ImpMotionSensor(pin=17, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(LuminositySensor(ImpLuminositySensor(pin=1, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(NoiseSensor(ImpNoiseSensor(pin=0, GPIO_ADC=shared), launcher.dataManager))
    launcher.aggiungiSensore(LedSensor(LampManager.getInstance(shared), launcher.dataManager))

    launcher.aggiungiElaborazione(PreElaborationMotion())
    launcher.aggiungiElaborazione(PreElaborationLum())
    launcher.aggiungiElaborazione(PreElaborationNoise())

    launcher.run()


if __name__ == "__main__":
    load_configs()
    atexit.register(commit_config)
    conf_server = ConfigurationServer()
    conf_server.start()
    main() if not Config.debug else main_debug()

