from threading import Thread
from web_server import app


class ConfigurationServer(Thread):

    def __init__(self):
        super(ConfigurationServer, self).__init__()
        self.app = app

    def run(self):
        app.run()
