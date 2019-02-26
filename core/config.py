"""Main settings for connection and sensors"""


class Config:

    """nome db locale"""
    local_db_name = 'localDB.db'

    """usato per controllare la raccolta dei dati nelle implementazioni dei sensori"""
    """debug = True --> i dati grezzi sono generati in modo random"""
    """debug = False --> i dati grezzi vengono raccolti dai sensori"""
    debug = True

    convertData = False

    """ip e porta su cui si è in ascolto per la ricezione degli alert dall'esterno"""
    listener_port = 12965
    listener_ip = "192.168.1.22"

    """info su Lampione (memorizzati anche all'interno di una tabella del db locale) """
    idLampione = 0
    idArea = 0
    lat = 0
    lon = 0
    """ip statico del raspberry"""
    static_ip = '192.168.1.22'
    prevLamp = None
    nextLamp = None
    """ prevLamp = None -> è il primo lampione dell'area """
    """ nextLamp = None -> è l'ultimo lampione dell'area """
