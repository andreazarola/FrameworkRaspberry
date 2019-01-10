from abc import ABC, abstractmethod


class AbstractLogger(ABC):

    @abstractmethod
    def printline(self, line):
        pass
