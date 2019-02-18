from base.sensor import Sensore


class LuminositySensor(Sensore):

    def __init__(self, imp, observer):
        super(LuminositySensor, self).__init__(imp,observer,"Luminosita")