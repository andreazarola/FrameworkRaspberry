from core.pre_elaborazione.abstract_pre_elaboration import AbstractPreElaboration
from core.pre_elaborazione.db_requestdatafactory import DBRequestDataFactory


class PreElaborationNoise(AbstractPreElaboration):

    def __init__(self):
        super(PreElaborationNoise, self).__init__("Rumore")

    def execute(self, giorno, ora, timestamp):
        """
        :param giorno: giorno della settimana di cui sto calcolando la media
        :param ora: ora del giorno di cui sto calcolando la media
        :return: true se il calcolo il salvataggio va bene, false altrimenti
        """
        request=DBRequestDataFactory().createRequest()
        request.setTipo(self.tipo)
        request.setHour(ora)
        request.setWeekDay(giorno)
        request.execute()

        """
        Calcolo del valore medio di rumorosita
        """
        somma, count = 0.0, 0
        for value in request.fetchAll():
            somma += value
            count += 1

        media = float(somma/count)

        print("Valore medio di " + giorno +
              " alle ore " + str(ora) + ": " + str(media))
