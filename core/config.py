"""Main settings for connection and sensors"""


class Config:

    """indirizzo es da remoto"""
    es_host = [{'host': '192.168.1.22', 'port': 9200}]

    es_host1 = [{'host': '192.168.43.16', 'port': 9200}]

    hive_connection = {
        'host_name': 'localhost',
        'port': 10000,
        'user': 'hive',
        'password': '',
        'db_name': 'default'
    }

    """nome db locale"""
    local_db_name = 'localDB.db'

    """usato per controllare la raccolta dei dati nelle implementazioni dei sensori"""
    """debug = True --> i dati grezzi sono generati in modo random"""
    """debug = False --> i dati grezzi vengono raccolti dai sensori"""
    debug = True

    convertData = False

    """pin del raspberry utilizzato per comunicare con il lampione"""
    lamp_pin = 18


    """ip e porta su cui si è in ascolto per la ricezione degli alert dall'esterno"""
    listener_port = 12965
    listener_ip = "localhost"

    """info su Lampione (memorizzati anche all'interno di una tabella del db locale) """
    idLampione = 0
    idArea = 0
    lat = 0
    lon = 0
    """ip statico del raspberry"""
    static_ip = '192.168.1.2'
    prevLamp = None
    nextLamp = None
    """ prevLamp = None -> è il primo lampione dell'area """
    """ nextLamp = None -> è l'ultimo lampione dell'area """
