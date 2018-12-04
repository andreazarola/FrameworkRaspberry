from core.pre_elaborazione.abstract_pre_elaboration import AbstractPreElaboration
from core.pre_elaborazione.db_requestdatafactory import DBRequestDataFactory


class PreElaborationMotion(AbstractPreElaboration):

    def __init__(self):
        super(PreElaborationMotion, self).__init__("Presenza")

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
        Calcolo della frequenza di presenza nell'arco di tutte le misure
        """
        num_presenze, count = 0, 0
        for value in request.fetchAll():
            num_presenze += value
            count += 1

        media = float(num_presenze/count)

        print("Frequenza relativa del Rumore di " + giorno +
              " alle ore " + str(ora) + ": " + str(media))
