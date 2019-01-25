from threading import Lock, Condition


class AlertQueue:

    _instance = None

    @staticmethod
    def get_instance():
        if AlertQueue._instance is None:
            AlertQueue._instance = AlertQueue()
        return AlertQueue._instance

    def __init__(self):
        self.queue = list()
        self.lock = Lock()
        self.cond = Condition(self.lock)

    def push(self, alert):
        try:
            self.lock.acquire()

            self.queue.append(alert)

            self.cond.notify()

        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def pop(self):
        try:
            self.lock.acquire()
            while len(self.queue) == 0:
                self.cond.wait()

            alert = self.queue.pop()

            return alert

        except Exception as e:
            print(e)

        finally:
            self.lock.release()
