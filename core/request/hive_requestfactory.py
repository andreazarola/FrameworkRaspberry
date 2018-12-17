from request.request_factory import RequestFactory
from request.hive_request import HiveRequest


class HiveRequestFactory(RequestFactory):

    def __init__(self):
        super(HiveRequestFactory, self).__init__()

    def createRequest(self):
        return HiveRequest()
