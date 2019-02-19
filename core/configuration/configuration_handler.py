from configuration.param import Param
from threading import Lock


class ConfigurationHandler:

    _instance = None

    @staticmethod
    def get_instance(file = None):
        if ConfigurationHandler._instance is None:
            ConfigurationHandler._instance = ConfigurationHandler(file)
        return ConfigurationHandler._instance

    def __init__(self, file):
        self.param_list = list()
        self.file = file
        self.lock = Lock()

    def add_param(self, line):
        data = line.split(',')
        p = Param()
        p.nome = data[0]
        p.tipo = data[1]
        p.valore = data[2]
        self.param_list.append(p)

    def get_param(self, name):
        param = None
        lock = None
        for p in self.param_list:
            if p.get_nome() == name:
                lock = p.get_lock()
                param = p
        if param is None:
            return None
        try:
            lock.acquire()

            if param.get_tipo() == "text":
                if param.get_valore() == "NULL":
                    return ""
                return param.get_valore()
            elif param.get_tipo() == "number":
                if param.get_valore() == "NULL":
                    return 0
                else:
                    return int(param.get_valore())
            elif param.get_tipo() == "real":
                if param.get_valore() == "NULL":
                    return 0
                else:
                    return float(param.get_valore())
            else:
                return param.get_valore()
        except Exception as e:
            print(e)
        finally:
            lock.release()

    def set_param(self, name, value):
        param = None
        lock = None
        for p in self.param_list:
            if p.get_nome() == name:
                lock = p.get_lock()
                param = p
        if param is None:
            return None
        try:
            self.lock.acquire()
            lock.acquire()

            param.set_valore(value)

        except Exception as e:
            print(e)
        finally:
            lock.release()
            self.lock.release()

    def get_es_params(self):
        pass

    def get_hive_params(self):
        pass

    def save_config(self):
        try:
            self.lock.acquire()

            f = open(self.file, 'w')
            f.write('Nome,Tipo,Valore\n')
            for p in self.param_list:
                f.write(p.get_nome() + ',' + p.get_tipo() + ',' + str(p.get_valore()) + '\n')
            f.flush()
            f.close()
            print("File salvato")
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def get_all(self):
        try:
            self.lock.acquire()

            return self.param_list

        except Exception as e:
            print(e)
        finally:
            self.lock.release()
