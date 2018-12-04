from core.local_db.dbconnection_factory import DBConnectionFactory
import re


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class DBRequestData:

    def __init__(self):
        self.conn = DBConnectionFactory().createConnection("localDB.db")
        self.tipo = None
        self.hour = None
        self.weekDay = None
        self.re = None
        self.lista_valori = list()

    def setTipo(self, tipo):
        self.tipo = tipo
        return self

    def setHour(self, hour):
        if hour < 10:
            self.hour = "0" + str(hour)
        else:
            self.hour = str(hour)
        return self

    def setWeekDay(self, day):
        self.weekDay = day
        return self

    def execute(self):
        try:
            self.re = str(self.weekDay) + ",\s\d{2}\.\s[a-zA-Z]+\s\d{4}\s" + self.hour + ":\d+.+"
        except TypeError:
            print("Valori di hour o weekDay errati")

        self.conn.create_function("REGEXP", 2, regexp)

        for val in self.conn.execute("SELECT d.dato "
                                     "FROM Dato as d "
                                     "WHERE d.tipo = ? and d.timestamp REGEXP \'" + self.re + "\'",
                                     (self.tipo,)):
            self.lista_valori.append(val[0])


    def fetchAll(self):
        """
        Restituisce una copia della lista dei valori restituiti
        dalla richiesta e svuota la lista interna
        :return: lista dei valori restituiti
        """
        list = self.lista_valori.copy()
        self.lista_valori.clear()
        return list

    def fetchOne(self):
        """
        Restituisce il primo elemento dalla lista dei valori restituiti
        dalla richiesta ed elimina l'elemento restituito dalla lista
        :return: primo elemento dalla lista
        """
        return self.lista_valori.pop(0)
