from core.request.request_factory import RequestFactory
from core.request.db_request import DBRequest


class DBRequestFactory(RequestFactory):

    def __init__(self):
        super(DBRequestFactory,self).__init__()

    def createRequest(self):
        return DBRequest()
