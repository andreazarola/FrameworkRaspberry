import sqlite3
import sys
from config import Config


class DBConnectionFactory:

    path = sys.path[0] + "/local_db/"

    def createConnection(self, dbName):
        return sqlite3.connect(self.path+dbName)
