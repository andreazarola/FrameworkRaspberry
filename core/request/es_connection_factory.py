from elasticsearch import Elasticsearch
from config import Config


class ESConnectionFactory:

    def createConnection(self):
        print(Config.es_host)
        return Elasticsearch(Config.es_host)
