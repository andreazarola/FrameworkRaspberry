from datetime import datetime
from logs.logger import Logger
from elasticsearch import helpers
from request.es_connection_factory import ESConnectionFactory
from local_db.dbconnection_factory import DBConnectionFactory

class ElaborateData:

    def __init__(self):
        """lista che mantiene i riferimenti agli implementatori che
           elaborano i dati
        """
        self.elaborate_list = list()
        self.data_list = list()
        self.idLamp = None
        self.index_ES = 'pre_elaborazione'

    def addImplementation(self, impl):
        self.elaborate_list.append(impl)

    """
    Funzione che viene eseguita ogni 60 minuti
    """
    def update(self):
        timestamp = datetime.now()
        info = timestamp.strftime("%A %H").split(" ")
        #print(info[0] + " " + info[1])
        Logger.getInstance().printline(info[0] + " " + info[1])

        ora = int(info[1]) - 1
        giorno = info[0]

        """
        caso in cui mi trovo a mezzanotte
        """
        if ora < 0:
            ora = 23
            giorno = self.giornoPrec(giorno)

        for imp in self.elaborate_list:
            imp.execute(giorno, ora, timestamp)
            data = imp.save_localdb()
            self.data_list.append(data)

        self.sendAll()
        self.data_list.clear()


    def sendAll(self):
        """
        Invia i dati appena elaborati ad ES
        :return: None
        """
        if self.idLamp is None:
            self.readInfoLamp()

        actions = [
            {
                '_index': self.index_ES,
                '_type': '_doc',
                '_source': {
                    'id_lamp': str(self.idLamp),
                    'type_data': data['tipo_dato'],
                    'value': data['value'],
                    'giorno': data['giorno'],
                    'ora': data['ora'],
                    'timestamp': data['timestamp']
                }
            }
            for data in self.data_list
        ]
        helpers.bulk(ESConnectionFactory().createConnection(), actions)

    def readInfoLamp(self):
        connection = DBConnectionFactory.create_connection()
        for row in connection.execute('SELECT id_lampione FROM Info'):
            self.idLamp = row[0]

    def giornoPrec(self, giorno):
        """
        :param giorno: nome del giorno di cui restituire quello precendente
        :return: restituisce il giorno precedente a quello ricevuto
        """
        if giorno == "Monday":
            return "Sunday"
        elif giorno == "Tuesday":
            return "Monday"
        elif giorno == "Wednesday":
            return "Tuesday"
        elif giorno == "Thursday":
            return "Wednesday"
        elif giorno == "Friday":
            return "Thursday"
        elif giorno == "Saturday":
            return "Friday"
        elif giorno == "Sunday":
            return "Saturday"
