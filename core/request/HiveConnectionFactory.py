from pyhive import hive


class HiveConnectionFactory:

    """
    Settare questi paramentri prima di richiedere una connessione ad Hive
    """
    host = None
    port = None
    username = None
    database = None

    def createConnection(self):
        return hive.connect(host=self.host,
                            port=self.port,
                            username=self.username,
                            database=self.database)
