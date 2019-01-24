from socketserver import BaseRequestHandler
import json


class ConnectionHandler(BaseRequestHandler):


    def handle(self):
        """indirizzo ip del client"""
        print("From " + str(self.client_address[0]))

        """socket usata per comunicare con il client"""
        recv_sock = self.request

        """lettura dei dati e parsing"""
        jsonString = str(recv_sock.recv(1024).strip())[2:-1]
        alert = json.loads(jsonString)

    """gestione dell'alert"""