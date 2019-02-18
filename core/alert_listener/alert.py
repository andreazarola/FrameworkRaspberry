from abc import ABC, abstractmethod
from local_db.dbconnection_factory import DBConnectionFactory
from base.lamp_manager import LampManager, MAX_DC, MIN_DC
from logs.logger import Logger


class AbstractAlert(ABC):
    """
    Classe che deve essere estesa per creare
    un nuovo tipo di alert da gestire
    """
    def __init__(self, info):
        self.info = info

    @abstractmethod
    def handle(self):
        pass


class ResetDataAlert(AbstractAlert):
    """
    Alert invocato per resettare i dati
    pre elaborati che vengono aggiornati ogni ora.
    """

    def handle(self):
        Logger.getInstance().printline("Reset pre_elaborati")
        conn = DBConnectionFactory.create_connection()
        conn.execute('UPDATE Pre_elaborato '
                     'SET valore = 0.0, numCampioni = 0')
        conn.commit()
        conn.close()


class MaxLightAlert(AbstractAlert):
    """
    Alert che viene invocato per settare
    il lampione alla massima intensita.
    """

    def handle(self, lamp):
        Logger.getInstance().printline("Luce massima lampione")
        lamp.set_dc(MAX_DC)


class MinLightAlert(AbstractAlert):

    def handle(self, lamp):
        Logger.getInstance().printline("Luce minima lampione")
        lamp.set_dc(MIN_DC)


class SetLightAlert(AbstractAlert):

    def handle(self, lamp,):
        Logger.getInstance().printline("Settato luce a: " + str(self.info['valore']))
        lamp.set_dc(int(self.info['valore']))


class UnknownAlert(Exception):
    pass
