from datetime import datetime
from logs.logger import Logger


class ElaborateData:

    def __init__(self):
        """lista che mantiene i riferimenti agli implementatori che
           elaborano i dati
        """
        self.elaborate_list = list()

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
        caso in cui mi trova a mezzanotte
        """
        if ora < 0:
            ora = 23
            giorno = self.giornoPrec(giorno)

        for imp in self.elaborate_list:
            imp.execute(giorno, ora, timestamp)
            imp.save_localdb()

        self.sendAll()


    def sendAll(self):
        """
        Da implementare
        :return: None
        """
        pass

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
