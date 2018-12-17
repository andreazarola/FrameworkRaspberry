from dataManager.data_manager import DataManager
from dataManager.dataElement import dataElement
from local_db.dbconnection_factory import DBConnectionFactory
from request.db_requestfactory import DBRequestFactory
from request.hive_requestfactory import HiveRequestFactory
from threading import Lock


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

            if not self.contenuto(data):
                #######################################################
                # Salvataggio del dato sul db locale
                request = DBRequestFactory().createRequest().initialize()
                request.setTimeStamp(sensore.lastTime)
                request.setTipoDato(sensore.tipoSensore)
                request.setValue(sensore.state)
                request.execute()
                #######################################################

                """aggiunta del dato alla lista dei dati da inviare"""
                self.data_to_hive_list.append(data)
            else:
                pass

            if len(self.data_to_hive_list) == len(self.sensor_list):
                """invio dei dati dell'ultimo minuto ad hive"""
                self.sendToHive()

        finally:
            self.updateLock.release()

    def contenuto(self, data):
        if len(self.data_to_hive_list) > 0:
            for d in self.data_to_hive_list:
                if d.tipo == data.tipo:
                 return True
        return False

    def sendToHive(self):
        #########################################
        print("Invio dati grezzi di tutti i sensori ad hive")
        #########################################
        """
        prendo dal db locale le info sul lampione (area,id,geotag)
        """
        info = self.getInfoLamp()
        print(info)
        #request = HiveRequestFactory().createRequest().setInfoLamp(info)
        #request.setData(self.data_to_hive_list)
        #request.execute()

        """
        resetto la lista di dati da mandare dopo che la mando ad hive
        """
        self.data_to_hive_list.clear()
        pass

    def getInfoLamp(self):
        connection = DBConnectionFactory().createConnection("localDB.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * "
                       "FROM Info")
        info = None
        try:
            row = cursor.fetchone()
            info = {"idLamp": row[0],
                    "area": row[1],
                    "lat": row[2],
                    "lon": row[3]}
        except TypeError:
            print("Dati non inviati esternamente")
            print("Necessario settare info sul dispositivo")

        return info
