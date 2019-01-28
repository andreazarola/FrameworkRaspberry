import sqlite3
import sys
from config import Config


class DBConnectionFactory:

    path = sys.path[0] + "/local_db/"

    @staticmethod
    def create_connection():
        return sqlite3.connect(DBConnectionFactory.path + Config.local_db_name)
