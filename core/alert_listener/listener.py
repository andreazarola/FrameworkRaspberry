from threading import Thread
from socketserver import ThreadingTCPServer
from config import Config
from alert_listener.connection_handler import ConnectionHandler


class AlertListener(Thread):

    def __init__(self):
        super(AlertListener, self).__init__()
        self.server = ThreadingTCPServer((Config.listener_ip, Config.listener_port), ConnectionHandler)

    def run(self):
        self.server.serve_forever()

    def close_server(self):
        self.server.server_close()
