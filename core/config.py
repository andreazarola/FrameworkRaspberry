"""Main settings for connection and sensors"""


class Config:

    """indirizzo es da remoto"""
    es_host = [{'host': '192.168.1.22', 'port': 9200}]

    es_host1 = [{'host': '192.168.43.16', 'port': 9200}]

    """nome db locale"""
    local_db_name = 'localDB.db'

    """usato per controllare la raccolta dei dati nelle implementazioni dei sensori"""
    """debug = True --> i dati grezzi sono generati in modo random"""
    """debug = False --> i dati grezzi vengono raccolti dai sensori"""
    debug = True

    convertData = False

    lamp_pin = 18

    listener_port = 12965
    listener_ip = "localhost"