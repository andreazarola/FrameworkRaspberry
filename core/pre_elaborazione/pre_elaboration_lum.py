from pre_elaborazione.abstract_pre_elaboration import AbstractPreElaboration
from pre_elaborazione.db_requestdatafactory import DBRequestDataFactory
from local_db.dbconnection_factory import DBConnectionFactory


class PreElaborationLum(AbstractPreElaboration):

    def __init__(self):
        super(PreElaborationLum, self).__init__("Luminosita")

    def execute(self, giorno, ora, stamp):
        """
        :param giorno: giorno della settimana di cui sto calcolando la media
        :param ora: ora del giorno di cui sto calcolando la media
        :param stamp: timestamp del momento in cui sto calcolando il valore
        :return: true se il calcolo il salvataggio va bene, false altrimenti
        """
        self.lastDay = giorno
        self.lastHour = ora
        self.timestamp = stamp.strftime("%A, %d. %B %Y %H:%M:%S")
        request = DBRequestDataFactory().createRequest()
        request.setTipo(self.tipo)
        request.setHour(self.lastHour)
        request.setWeekDay(self.lastDay)
        request.execute()

        """
        Calcolo del valore medio di rumorosita
        """
        somma, count = 0.0, 0
        for value in request.fetchAll():
            somma += value
            count += 1

        self.value = float(somma/count)

        print("Valore medio di " + self.tipo + " di " + giorno +
              " alle ore " + str(ora) + ": " + str(self.value))

    def save_localdb(self):
        conn = DBConnectionFactory().createConnection("localDB.db")
        exist = False
        for row in conn.execute("SELECT * "
                                "FROM Pre_elaborato "
                                "WHERE tipo = ? and giorno = ? and ora = ?",
                                (self.tipo, self.lastDay, self.lastHour)):
            exist = True

        if exist:
            conn.execute("UPDATE Pre_elaborato "
                         "SET valore = ?, timestamp = ? "
                         "WHERE tipo = ? and giorno = ? and ora = ?",
                         (self.value, self.timestamp, self.tipo, self.lastDay, self.lastHour))
        else:
            conn.execute("INSERT INTO Pre_elaborato values (?, ?, ?, ?, ?)",
                         (self.tipo, self.lastDay, self.lastHour, self.value, self.timestamp))

        conn.commit()
        conn.close()
