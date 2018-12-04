from abc import ABC, abstractmethod


class AbstractPreElaboration(ABC):

    def __init__(self, tipo):
        self.tipo=tipo

    @abstractmethod
    def execute(self, giorno, ora, timestamp):
        pass
