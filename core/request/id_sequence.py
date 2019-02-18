from local_db.dbconnection_factory import DBConnectionFactory
from threading import RLock


class SequenzaId:

    _instance = None

    @staticmethod
    def get_instance():
        if SequenzaId._instance is None:
            SequenzaId._instance = SequenzaId()
        return SequenzaId._instance

    def __init__(self):
        self.connection = DBConnectionFactory.create_connection()
        self.current = 0
        self.last = -1
        self.lock = RLock()
        c = self.connection.cursor()
        c.execute('SELECT max(id) as max '
                  'FROM Dato')
        row = c.fetchall()
        for r in row:
            if r[0] is not None:
                self.current = int(r[0]) + 1
                self.last = int(r[0])

    def get_id(self):
        try:
            self.lock.acquire()
            new_id = self.current
            self.last = new_id
            self.current += 1
            return new_id
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def get_last(self):
        try:
           self.lock.acquire()
           return self.last
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
