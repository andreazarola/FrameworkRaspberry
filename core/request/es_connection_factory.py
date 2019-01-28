from elasticsearch import Elasticsearch
from config import Config


class ESConnectionFactory:

    def createConnection(self):
        return Elasticsearch(Config.es_host)
