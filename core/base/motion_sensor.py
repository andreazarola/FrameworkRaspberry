from base.sensor import Sensore

class MotionSensor(Sensore):

    def __init__(self,imp,observer):
        super(MotionSensor, self).__init__(imp, observer, "Presenza")