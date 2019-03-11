"""
    Classe di configurazione utilizzata in fase di sviluppo
    Non modificare!
"""


class Config:

    """nome db locale"""
    local_db_name = 'localDB.db'

    """usato per controllare la raccolta dei dati nelle implementazioni dei sensori"""
    """debug = True --> i dati grezzi sono generati in modo random"""
    """debug = False --> i dati grezzi vengono raccolti dai sensori"""
    debug = True

    convertData = False

    """porta su cui si è in ascolto per la ricezione degli alert dall'esterno"""
    alert_listener_port = 12965
    """porta su cui è in ascolto il web server flask"""
    flask_port = 5000
