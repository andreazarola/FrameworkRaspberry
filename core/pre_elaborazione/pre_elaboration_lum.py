from pre_elaborazione.abstract_pre_elaboration import AbstractPreElaboration
from pre_elaborazione.db_requestdatafactory import DBRequestDataFactory
from local_db.dbconnection_factory import DBConnectionFactory
from configuration.configuration_handler import ConfigurationHandler
from logs.logger import Logger


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
        request.setHour(ora)
        request.setWeekDay(giorno)
        request.execute()

        lastSum, count = 0.0, 0
        for value in request.fetchAll():
            lastSum += value
            count += 1

        current_average = float(lastSum / count)

        info = self.get_info()

        n_campioni_max = ConfigurationHandler.get_instance().get_param('nCampioniRiferimento')

        if info['numCampioni'] < n_campioni_max:
            total = (round(info['numCampioni'] * info['valore_corrente']) + current_average)
            campioni_totali = (info['numCampioni'] + 1)
            total_average = round(total/campioni_totali)
            self.nCampioni = campioni_totali
            self.value = total_average
        else:
            total = (round(n_campioni_max * info['valore_corrente']) + current_average)
            campioni_totali = n_campioni_max + 1
            total_average = round(total/campioni_totali)
            self.nCampioni = campioni_totali
            self.value = total_average

        Logger.getInstance().printline("Valore medio di " + self.tipo + " di " + giorno +
                                       " alle ore " + str(ora) + ": " + str(self.value))

    def get_info(self):
        conn = DBConnectionFactory.create_connection()
        numCampioni = 0
        value = 0
        for row in conn.execute("SELECT numCampioni, valore "
                                "FROM Pre_elaborato "
                                "WHERE tipo = ? and giorno = ? and ora = ?",
                                (self.tipo, self.lastDay, self.lastHour)):
            numCampioni = row[0]
            value = row[1]
        conn.close()
        return {'numCampioni': numCampioni, 'valore_corrente': value}

    def save_localdb(self):
        """
        Salva o aggiorna il valore elaborato sul db locale
        :return: il documento da inviare ad ES
        """
        conn = DBConnectionFactory.create_connection()
        exist = False
        for row in conn.execute("SELECT * "
                                "FROM Pre_elaborato "
                                "WHERE tipo = ? and giorno = ? and ora = ?",
                                (self.tipo, self.lastDay, self.lastHour)):
            exist = True

        if exist:
            conn.execute("UPDATE Pre_elaborato "
                         "SET valore = ?, numCampioni = ?, timestamp = ? "
                         "WHERE tipo = ? and giorno = ? and ora = ?",
                         (self.value, self.nCampioni, self.timestamp, self.tipo, self.lastDay, self.lastHour))
        else:
            conn.execute("INSERT INTO Pre_elaborato values (?, ?, ?, ?, ?, ?)",
                         (self.tipo, self.lastDay, self.lastHour, self.nCampioni, self.value, self.timestamp))

        conn.commit()
        conn.close()
        return {
                'tipo_dato': self.tipo,
                'value': str(round(self.value, 3)),
                'giorno': str(self.lastDay),
                'ora': str(self.lastHour),
                'timestamp': self.timestamp
        }
