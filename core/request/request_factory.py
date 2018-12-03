from abc import ABC,abstractmethod


class RequestFactory(ABC):

    @abstractmethod
    def createRequest(self):
        pass