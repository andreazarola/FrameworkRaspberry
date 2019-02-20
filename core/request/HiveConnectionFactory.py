from pyhive import hive
from configuration.configuration_handler import ConfigurationHandler


class HiveConnectionFactory:

    @staticmethod
    def create_connection():
        conf = ConfigurationHandler.get_instance()
        password = conf.get_param('hive_connection_password')
        if password is not '':
            return hive.Connection(host=conf.get_param('hive_connection_ip'),
                                   port=conf.get_param('hive_connection_port'),
                                   username=conf.get_param('hive_connection_user'),
                                   password=password,
                                   database=conf.get_param('hive_db_name'),
                                   configuration={'mapred.job.tracker': 'local'})
        else:
            return hive.Connection(host=conf.get_param('hive_connection_ip'),
                                   port=conf.get_param('hive_connection_port'),
                                   username=conf.get_param('hive_connection_user'),
                                   database=conf.get_param('hive_db_name'),
                                   configuration={'mapred.job.tracker': 'local'})