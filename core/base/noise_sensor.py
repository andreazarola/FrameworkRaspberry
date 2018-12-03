from core.base.sensor import Sensore


class NoiseSensor(Sensore):

    def __init__(self,imp,observer):
        super(NoiseSensor, self).__init__(imp, observer, "Rumore")