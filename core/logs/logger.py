from logs.abstract_logger import AbstractLogger
from logs.real_logger import RealLogger
from datetime import datetime, timezone


class Logger(AbstractLogger):

    __instance = None

    def __init__(self):
        self.internal_logger = None
        super(AbstractLogger, self).__init__()

    @staticmethod
    def getInstance():
        if Logger.__instance is None:
            Logger.__instance = Logger()
        return Logger.__instance

    def printline(self, line):
        if self.internal_logger is not None:
            return self.internal_logger.printline(line)

        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print('[' + time + ']\t' + line)
        return None

    def init_logger(self, path):
        self.internal_logger = RealLogger(path)
