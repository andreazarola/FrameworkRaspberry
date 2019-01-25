from threading import Thread


class AlertExecutor(Thread):

    def __init__(self, alert_queue):
        super(AlertExecutor, self).__init__()
        self.queue = alert_queue

    def run(self):
        while True:
            alert = self.queue.pop()

            print("preso alert dalla queue")
            print(alert)
            self.handle_alert(alert)
            print("alert gestito")

    def handle_alert(self, alert):
        pass
