from dataManager.data_manager import DataManager
from dataManager.dataElement import dataElement
from local_db.dbconnection_factory import DBConnectionFactory
from request.db_requestfactory import DBRequestFactory
from request.hive_requestfactory import HiveRequestFactory
from request.hive_threading_request import HiveThreadingRequest
from configuration.configuration_handler import ConfigurationHandler
from logs.logger import Logger
from threading import Lock
import json


class InstantDataManager(DataManager):

    def __init__(self):
        super(InstantDataManager, self).__init__()
        self.updateLock = Lock()
        """
        lista che mantiene le triple (tipo,valore,timestamp) dei
        sensori che hanno raccolto i dati
        """
        self.data_to_hive_list = list()

    def attach_sensor(self, tipo_sensore):
        try:
            self.updateLock.acquire()

            self.sensor_list.append(tipo_sensore)

        finally:
            self.updateLock.release()

    def detach_sensor(self, tipo_sensore):
        try:
            self.updateLock.acquire()

            self.sensor_list.remove(tipo_sensore)

        finally:
            self.updateLock.release()

    def update(self, sensore):
        try:
            self.updateLock.acquire()

            data = dataElement(sensore.tipoSensore, sensore.state, sensore.lastTime)

            """
            Salvataggio del dato sul db locale
            """
            request = DBRequestFactory().createRequest().initialize()
            request.setTimeStamp(sensore.lastTime)
            request.setTipoDato(sensore.tipoSensore)
            request.setValue(sensore.state)
            request.execute()

            """aggiunta del dato alla lista dei dati da inviare"""
            self.data_to_hive_list.append(data)

            if len(self.data_to_hive_list) >= ConfigurationHandler.get_instance().get_param("max_number_to_hive"):
                """invio dei dati ad hive"""
                self.sendToHive()

        finally:
            self.updateLock.release()

    def sendToHive(self):
        Logger.getInstance().printline("Invio dati grezzi di tutti i sensori ad hive")
        """
        prendo dal db locale le info sul lampione
        """
        info = self.getInfoLamp()
        Logger.getInstance().printline(json.dumps(info))

        request = HiveRequestFactory().createRequest().setInfoLamp(info)
        request.setData(self.data_to_hive_list[:])
        request.setTableName("dato")

        send_request = HiveThreadingRequest(request)
        send_request.start()

        """
        resetto la lista di dati da mandare dopo che la mando ad hive
        """
        self.data_to_hive_list.clear()

    def getInfoLamp(self):
        connection = DBConnectionFactory.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id_lampione, idArea, latitudine, longitudine, static_ip "
                       "FROM Info")
        info = None
        try:
            row = cursor.fetchone()
            info = {"idLamp": row[0],
                    "idArea": row[1],
                    "lat": row[2],
                    "lon": row[3],
                    "static_ip": row[4]}
        except TypeError:
            Logger.getInstance().printline("Dati non inviati esternamente")
            Logger.getInstance().printline("Necessario settare info sul dispositivo")

        return info
