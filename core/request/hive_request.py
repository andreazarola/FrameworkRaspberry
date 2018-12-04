from core.request.abstract_request import Request
from core.request.HiveConnectionFactory import HiveConnectionFactory


class HiveRequest(Request):

    def __init__(self):
        super(HiveRequest, self).__init__()
        self.connection=HiveConnectionFactory().createConnection()
        self.info = None
        self.dataList = None

    def setInfoLamp(self, info):
        self.info = info
        return self

    def setData(self,data):
        self.dataList = data
        return self

    def initialize(self):
        pass

    def execute(self):
        pass
