import sqlite3


class DBConnectionFactory:

    path = "/home/andrea/PycharmProjects/framework/core/local_db/"

    def createConnection(self, dbName):
        return sqlite3.connect(self.path+dbName)
