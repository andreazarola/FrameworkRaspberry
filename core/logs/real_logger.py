from logs.abstract_logger import AbstractLogger
from threading import Lock


class RealLogger(AbstractLogger):

    def __init__(self, path):
        self.log_file = path+"/logs/framework.log"
        self.locker_log = Lock()
        super(AbstractLogger, self).__init__()

    def printline(self, line):
        try:

            self.locker_log.acquire()

            f = open(self.log_file, "a+")
            f.write(line + "\n")
            f.close()

        except IOError:
            raise KeyboardInterrupt
        finally:
            self.locker_log.release()
        return None