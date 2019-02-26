class Trigger:

    def __init__(self, nome='', hour='*', minute='*', second='*'):
        self.nome = nome
        self.hour = hour
        self.minute = minute
        self.second = second

    def get_nome(self):
        return self.nome

    def get_hour(self):
        return self.hour

    def get_minute(self):
        return self.minute

    def get_second(self):
        return self.second

    def set_hour(self, hour):
        self.hour = hour

    def set_minute(self, minute):
        self.minute = minute

    def set_second(self, second):
        self.second = second
