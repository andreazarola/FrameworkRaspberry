from core.request.request_factory import RequestFactory
from core.pre_elaborazione.db_requestdata import DBRequestData


class DBRequestDataFactory(RequestFactory):

    def __init__(self):
        super(DBRequestDataFactory, self).__init__()

    def createRequest(self):
        return DBRequestData()
