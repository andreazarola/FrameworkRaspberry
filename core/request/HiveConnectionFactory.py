from pyhive import hive
from configuration.configuration_handler import ConfigurationHandler


class HiveConnectionFactory:

    def createConnection(self):
        return hive.connect(host=ConfigurationHandler.get_param('hive_connection_ip'),
                            port=ConfigurationHandler.get_param('hive_connection_port'),
                            username=ConfigurationHandler.get_param('hive_connection_user'),
                            password=ConfigurationHandler.get_param('hive_connection_password'),
                            database=ConfigurationHandler.get_param('hive_db_name'))
