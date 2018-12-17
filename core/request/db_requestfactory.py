from request.request_factory import RequestFactory
from request.db_request import DBRequest


class DBRequestFactory(RequestFactory):

    def __init__(self):
        super(DBRequestFactory,self).__init__()

    def createRequest(self):
        return DBRequest()
