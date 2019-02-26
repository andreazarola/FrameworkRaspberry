from configuration.trigger import Trigger
from test.scheduler import Scheduler


class ConfigurationTrigger:

    _instance = None

    @staticmethod
    def get_instance(file=None):
        if ConfigurationTrigger._instance is None:
            ConfigurationTrigger._instance = ConfigurationTrigger(file)
        return ConfigurationTrigger._instance

    def __init__(self, file):
        self.trigger_list = list()
        self.file = file

    def add_trigger(self, line):
        trigger = line.split(';')
        t = Trigger(nome=trigger[0], hour=trigger[1], minute=trigger[2], second=trigger[3])
        self.trigger_list.append(t)

    def get_trigger(self, name):
        trigger = None
        for t in self.trigger_list:
            if t.get_nome() == name:
                trigger = t
        return trigger

    def set_trigger(self, name, hour='', minute='', second=''):
        trigger = None
        for t in self.trigger_list:
            if t.get_nome() == name:
                trigger = t
        if trigger is None:
            return False
        if hour != '':
            trigger.set_hour(hour)
        if minute != '':
            trigger.set_minute(minute)
        if second != '':
            trigger.set_second(second)
        print("trigger trovato")
        result = Scheduler.get_instance().edit_job(trigger.get_nome(),
                                         trigger.get_second(),
                                         trigger.get_minute(),
                                         trigger.get_hour())

        return result

    def save_triggers(self):
        f = open(self.file, 'w')
        f.write('Sensore,Hour,Minute,Second\n')
        for t in self.trigger_list:
            f.write(t.get_nome() + ';' + t.get_hour() + ';' + t.get_minute() + ';' + t.get_second() + '\n')
        f.flush()
        f.close()

    def get_all(self):
        return self.trigger_list
