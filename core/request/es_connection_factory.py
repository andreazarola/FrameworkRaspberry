from elasticsearch import Elasticsearch
from configuration.configuration_handler import ConfigurationHandler


class ESConnectionFactory:

    def createConnection(self):
        return Elasticsearch([{'host': ConfigurationHandler.get_instance().get_param('es_host_ip'),
                              'port': ConfigurationHandler.get_instance().get_param('es_host_port')}])
