from request.abstract_request import Request
from elasticsearch import ElasticsearchException as ESException
from logs.logger import Logger


class ES_SendRequest(Request):

    def __init__(self):
        super(ES_SendRequest, self).__init__()
        self.connection = None
        self.doc = None
        self.index = None
        self.response = None

    def initialize(self):
        self.doc = {}
        self.index = ''
        self.response = None
        return self

    def set_connection(self, es_connection):
        self.connection = es_connection
        return self

    def set_index(self, index):
        self.index = index
        return self

    def add_param_to_doc(self, key, value):
        self.doc[key] = value
        return self

    def execute(self):
        try:
            self.response = self.connection.index(self.index, doc_type='doc', body=self.doc)
        except ESException as e:
            Logger.getInstance().printline(str(e))

    def get_response(self):
        return self.response
