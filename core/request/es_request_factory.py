from request.request_factory import RequestFactory
from request.es_send_request import ES_SendRequest


class ES_RequestFactory(RequestFactory):

    def __init__(self):
        super(ES_RequestFactory, self).__init__()

    def createRequest(self):
        return ES_SendRequest()
