from threading import Thread
from socketserver import ThreadingTCPServer
from system_info import SystemInfo
from alert_listener.connection_handler import ConnectionHandler
from logs.logger import Logger


class AlertListener(Thread):

    def __init__(self):
        super(AlertListener, self).__init__()
        self.server = ThreadingTCPServer((SystemInfo.private_static_ip, SystemInfo.public_alert_port), ConnectionHandler)

    def run(self):
        Logger.getInstance().printline("Alert listener in ascolto su: [" + SystemInfo.private_static_ip + ", " +
                                       str(SystemInfo.public_alert_port) + "]")
        self.server.serve_forever()

    def close_server(self):
        self.server.server_close()
