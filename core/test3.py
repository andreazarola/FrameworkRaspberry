from test.launcher import Launcher
from local_db.init_db import init_db
from base.motion_sensor import MotionSensor
from base.noise_sensor import NoiseSensor
from base.lum_sensor import LuminositySensor
from base.led_sensor import LedSensor
from base.rain_sensor import RainSensor
from base.lamp_manager import LampManager
from sensor_implementation.impLumSensor import ImpLuminositySensor
from sensor_implementation.impNoiseSensor import ImpNoiseSensor
from sensor_implementation.impMotionSensor import ImpMotionSensor
from sensor_implementation.impRainSensor import ImpRainSensor
from pre_elaborazione.pre_elaboration_noise import PreElaborationNoise
from pre_elaborazione.pre_elaboration_motion import PreElaborationMotion
from pre_elaborazione.pre_elaboration_lum import PreElaborationLum
from pre_elaborazione.pre_elaboration_rain import PreElaborationRain
from logs.logger import Logger
from configuration.configuration_handler import ConfigurationHandler
from configuration.configuration_trigger import ConfigurationTrigger
from config_server import ConfigurationServer
from config import Config
import sys
import atexit


def commit_config():
    ConfigurationHandler.get_instance().save_config()
    ConfigurationTrigger.get_instance().save_triggers()


def load_configs():
    path = sys.path[0]
    config_file = path + '/configuration_file'
    file = open(config_file, 'r')
    conf_handler = ConfigurationHandler.get_instance(config_file)
    for line in file.readlines()[1:]:
        conf_handler.add_param(line.rstrip())
    file.close()

    trigger_file= path + '/configuration_trigger_sensor'
    file = open(trigger_file, 'r')
    trigger_handler = ConfigurationTrigger.get_instance(trigger_file)
    for line in file.readlines()[1:]:
        trigger_handler.add_trigger(line.rstrip())
    file.close()


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
    motion = MotionSensor(ImpMotionSensor(pin=17, GPIO_ADC=shared), launcher.dataManager)
    rain = RainSensor(ImpRainSensor(pin=27, GPIO_ADC=shared), launcher.dataManager)
    luminosity = LuminositySensor(ImpLuminositySensor(pin=1, GPIO_ADC=shared), launcher.dataManager)
    noise = NoiseSensor(ImpNoiseSensor(pin=0, GPIO_ADC=shared), launcher.dataManager)
    led_sensor = LedSensor(LampManager.getInstance(shared), launcher.dataManager)
    launcher.aggiungiSensore(motion)
    launcher.aggiungiSensore(rain)
    launcher.aggiungiSensore(luminosity)
    launcher.aggiungiSensore(noise)
    launcher.aggiungiSensore(led_sensor)
    launcher.aggiungi_sensore_passivo(noise)
    launcher.aggiungi_sensore_passivo(led_sensor)
    launcher.aggiungi_sensore_passivo(luminosity)
    launcher.aggiungi_sensore_attivo(motion)
    launcher.aggiungi_sensore_attivo(rain)

    launcher.aggiungiElaborazione(PreElaborationMotion())
    launcher.aggiungiElaborazione(PreElaborationLum())
    launcher.aggiungiElaborazione(PreElaborationNoise())
    launcher.aggiungiElaborazione(PreElaborationRain())

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
    motion = MotionSensor(ImpMotionSensor(pin=17, GPIO_ADC=shared), launcher.dataManager)
    rain = RainSensor(ImpRainSensor(pin=27, GPIO_ADC=shared), launcher.dataManager)
    luminosity = LuminositySensor(ImpLuminositySensor(pin=1, GPIO_ADC=shared), launcher.dataManager)
    noise = NoiseSensor(ImpNoiseSensor(pin=0, GPIO_ADC=shared), launcher.dataManager)
    led_sensor = LedSensor(LampManager.getInstance(shared), launcher.dataManager)
    launcher.aggiungiSensore(motion)
    launcher.aggiungiSensore(rain)
    launcher.aggiungiSensore(luminosity)
    launcher.aggiungiSensore(noise)
    launcher.aggiungiSensore(led_sensor)
    launcher.aggiungi_sensore_passivo(noise)
    launcher.aggiungi_sensore_passivo(led_sensor)
    launcher.aggiungi_sensore_passivo(luminosity)
    launcher.aggiungi_sensore_attivo(motion)
    launcher.aggiungi_sensore_attivo(rain)

    launcher.aggiungiElaborazione(PreElaborationMotion())
    launcher.aggiungiElaborazione(PreElaborationLum())
    launcher.aggiungiElaborazione(PreElaborationNoise())
    launcher.aggiungiElaborazione(PreElaborationRain())

    launcher.run()


if __name__ == "__main__":
    load_configs()
    atexit.register(commit_config)
    conf_server = ConfigurationServer()
    conf_server.start()
    main() if not Config.debug else main_debug()

