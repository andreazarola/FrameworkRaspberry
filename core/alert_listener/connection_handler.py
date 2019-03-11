from socketserver import BaseRequestHandler
from datetime import datetime
from alert_listener.alert_queue import AlertQueue
from local_db.dbconnection_factory import DBConnectionFactory
import json
from logs.logger import Logger


class ConnectionHandler(BaseRequestHandler):

    def handle(self):
        Logger.getInstance().printline("From " + str(self.client_address[0]))

        """socket usata per comunicare con il client"""
        recv_sock = self.request

        """lettura dei dati e parsing"""
        json_string = str(recv_sock.recv(1024).strip())[2:-1]
        self.alert = json.loads(json_string)
        self.alert['timestamp_ricezione'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_alert_on_db()

        AlertQueue.get_instance().push(self.alert)

    """gestione dell'alert"""
    def save_alert_on_db(self):
        conn = DBConnectionFactory.create_connection()
        cursor = conn.cursor()
        time_stamp = datetime.strptime(self.alert['timestamp'], "%Y-%m-%d %H:%M:%S")
        time_stamp = time_stamp.strftime("%A, %d. %B %Y %H:%M:%S")
        time_stamp_ricezione = datetime.strptime(self.alert['timestamp_ricezione'], "%Y-%m-%d %H:%M:%S")
        time_stamp_ricezione = time_stamp_ricezione.strftime("%A, %d. %B %Y %H:%M:%S")
        cursor.execute('INSERT INTO Alert (tipo, valore, timestamp, timestamp_ricezione) values (?, ?, ?, ?)',
                       (self.alert['tipo_alert'], self.alert['valore'], time_stamp, time_stamp_ricezione))

        alert_id = cursor.lastrowid
        self.alert['id'] = alert_id

        conn.commit()
        conn.close()
