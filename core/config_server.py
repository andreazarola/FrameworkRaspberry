from threading import Thread
from web_server import app
from config import Config


class ConfigurationServer(Thread):

    def __init__(self):
        super(ConfigurationServer, self).__init__()
        self.app = app

    def run(self):
        app.run(host="0.0.0.0", port=Config.flask_port)
