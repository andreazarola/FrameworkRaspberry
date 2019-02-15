from threading import Lock


class Param:

    def __init__(self, nome="", tipo="", valore=None):
        self.nome = nome
        self.tipo = tipo
        self.valore = valore
        self.internalLock = Lock()

    def get_nome(self):
        return self.nome

    def get_tipo(self):
        return self.tipo

    def get_lock(self):
        return self.internalLock

    def get_valore(self):
        return self.valore

    def set_valore(self, valore):
        self.valore = valore