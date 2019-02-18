from base.sensor import Sensore


class LedSensor(Sensore):

    def __init__(self, imp, observer):
        super(LedSensor, self).__init__(imp, observer, "Intensita Led")
