from pyhive import hive
from config import Config


class HiveConnectionFactory:

    def createConnection(self):
        return hive.connect(host=Config.hive_connection['host_name'],
                            port=Config.hive_connection['port'],
                            username=Config.hive_connection['user'],
                            password=Config.hive_connection['password'],
                            database=Config.hive_connection['db_name'])
