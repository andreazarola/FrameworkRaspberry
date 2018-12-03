from core.request.abstract_request import Request
from core.local_db.connection_factory import ConnectionFactory
import sqlite3


class DBRequest(Request):
    
    def __init__(self):
        super(DBRequest, self).__init__()
        self.conn = ConnectionFactory().createConnection("localDB.db")
        self.conn.text_factory = str

    def setTipoDato(self, tipo):
        self.tipoDato = tipo
        return self

    def setValue(self, value):
        self.value = value
        return self

    def setTimeStamp(self, timestamp):
        self.TimeStamp = timestamp
        return self

    def initialize(self):
        self.tipoDato = None
        self.value = None
        self.TimeStamp = None
        return self

    def execute(self):
        if self.tipoDato == None or self.value == None or self.TimeStamp == None :
            raise Exception ("Non sono stati settati tutti i campi della richiesta")

        try:
            self.conn.execute("INSERT INTO Dato values (?,?,?)",
                              (str(self.TimeStamp),
                               self.tipoDato,
                               float(self.value)))
            self.done()
        except sqlite3.IntegrityError:
            print ("Errore di intregrità nei dati")
            #raise Exception ("Errore durante l'esecuzione della query")

    def done(self):
        self.conn.commit()
        self.conn.close()