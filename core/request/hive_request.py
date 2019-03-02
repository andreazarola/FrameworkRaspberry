from request.abstract_request import Request
from request.HiveConnectionFactory import HiveConnectionFactory
from logs.logger import Logger


class HiveRequest(Request):

    def __init__(self):
        super(HiveRequest, self).__init__()
        self.connection = None
        self.info = None
        self.dataList = None
        self.tableName = None

    def setInfoLamp(self, info):
        self.info = info
        return self

    def setTableName(self, table):
        self.tableName = table
        return self

    def setData(self, data):
        self.dataList = data
        return self

    def initialize(self):
        pass

    def execute(self):
        insert = ("INSERT INTO TABLE " + self.tableName + " VALUES ")
        rows = list()
        for data in self.dataList:
            rows.append(("(" + str(self.info['idLamp']) + ", \'" + data.tipo + "\', " + str(data.valore) +
                         ", \'" + data.timestamp + "\')"))
        insert = insert + (", ".join(rows))
        try:
            self.connection = HiveConnectionFactory.create_connection()
            cursor = self.connection.cursor()
            cursor.execute(insert)
            Logger.getInstance().printline("Inviati ad hive: " + str(len(self.dataList)) + " dati")
        except Exception as e:
            Logger.getInstance().printline(str(e))

    def close_connection(self):
        self.connection.close()
        Logger.getInstance().printline("Chiusura connessione ad hive")
