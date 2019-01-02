from abc import ABC, abstractmethod


class AbstractPreElaboration(ABC):

    def __init__(self, tipo):
        self.tipo = tipo
        self.value = None
        self.lastDay = None
        self.lastHour = None
        self.timestamp = None
        self.nCampioni = None

    @abstractmethod
    def execute(self, giorno, ora, stamp):
        pass

    @abstractmethod
    def save_localdb(self):
        pass
