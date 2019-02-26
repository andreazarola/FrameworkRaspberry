from base.sensor import Sensore


class RainSensor(Sensore):

    def __init__(self, imp, observer):
        super(RainSensor, self).__init__(imp, observer, "Pioggia")
