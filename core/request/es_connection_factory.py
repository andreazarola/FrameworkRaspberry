from elasticsearch import Elasticsearch


class ESConnectionFactory:

    def createConnection(self):
        return Elasticsearch()
