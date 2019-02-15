from request.abstract_request import Request
#from request.HiveConnectionFactory import HiveConnectionFactory
from logs.logger import Logger


class HiveRequest(Request):

    def __init__(self):
        super(HiveRequest, self).__init__()
    #    self.connection = HiveConnectionFactory().createConnection()
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
        insert = ("INSERT INTO TABLE " + self.tableName + " VALUES  ")
        rows = list()
        for data in self.dataList:
            rows.append(("(\'" + data.tipo + "\', " + str(data.valore) + ", \'" + data.timestamp + "\', " +
                         str(self.info['idLamp']) + ")"))
        insert = insert + (", ".join(rows))
        Logger.getInstance().printline(insert)
        pass
