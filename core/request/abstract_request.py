from abc import ABC,abstractmethod


class Request(ABC):

    #inizializza la richiesta con i dati contenuti in object
    @abstractmethod
    def initialize(self):
        pass

    #esegue la richiesta
    @abstractmethod
    def execute(self):
        pass