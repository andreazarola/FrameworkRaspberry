from threading import Thread
from alert_listener.alert import ResetDataAlert, MaxLightAlert, MinLightAlert, SetLightAlert, SetSafetyAlert, UnknownAlert
from local_db.dbconnection_factory import DBConnectionFactory
from logs.logger import Logger
import json


class AlertExecutor(Thread):
    """
    Classe che si occupa di prendere un alert alla volta, quando arrivano,
    dalla coda di alert e di invocarne l'esecuzione
    """

    def __init__(self, alert_queue, lamp_manager):
        super(AlertExecutor, self).__init__()
        self.queue = alert_queue
        self.lamp_manager = lamp_manager
        self.last_alert_time = None

    def run(self):
        while True:
            alert = self.queue.pop()

            Logger.getInstance().printline("preso alert dalla queue")
            Logger.getInstance().printline(json.dumps(alert))
            self.last_alert_time = alert['timestamp_ricezione']
            try:
                self.handle_alert(alert)
                self.update_alert(alert['id'])
                Logger.getInstance().printline("alert gestito")
            except Exception as e:
                Logger.getInstance().printline(str(e))

    def handle_alert(self, alert):
        tipo = alert['tipo_alert']
        if tipo == 'reset_dati':
            ResetDataAlert(alert).handle()
        elif tipo == 'max_light':
            MaxLightAlert(alert).handle(self.lamp_manager)
        elif tipo == 'min_light':
            MinLightAlert(alert).handle(self.lamp_manager)
        elif tipo == 'set_light':
            SetLightAlert(alert).handle(self.lamp_manager)
        elif tipo == 'set_safety':
            SetSafetyAlert(alert).handle()
        else:
            raise UnknownAlert("Tipo di alert non riconosciuto")

    def update_alert(self, id_alert):
        conn = DBConnectionFactory.create_connection()
        conn.execute('UPDATE Alert '
                     'SET eseguito = 1 '
                     'WHERE id = ?', (id_alert,))
        conn.commit()
        conn.close()
