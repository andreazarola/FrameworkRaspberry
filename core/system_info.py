"""
    Classe statica che contiene le informazioni sul lampione
    Va modificata per ogni lampione
"""


class SystemInfo:
    """
    :param idLampione: id del lampione all'interno dell'intero sistema
    :param idArea: id dell'area in cui si trova il lampione
    :param lat: latitudine del punto in cui si trova il lampione
    :param lon: longitudine del punto in cui si trova il lampione
    :param public_static_ip: ip publico che viene utilizzato per connettersi dall'esterno dell'AP
    :param prevLamp: id del prevLamp nell'intero sistema
    :param nextLamp: id del nextLamp nell'intero sistema
    :param public_alert_port: porta publica su cui e in ascolto l'alert listener
    :param public_web_server_port: porta publica sui cui e in ascolto flask
    :param postgres_ip: ip della macchina su cui è in esecuzione il db postgres
    :param postgres_port: porta su cui è in ascolto il db postgres sulla macchina
    :param postgres_user: utente con cui si accede al db postgres
    :param postgres_password: password per accedere al db postgres
    """

    idLampione = 1
    idArea = 1
    lat = 0
    lon = 0
    private_static_ip = '192.168.1.22'
    public_static_ip = '62.211.35.158'
    prevLamp = None
    nextLamp = None
    public_alert_port = 12965
    public_web_server_port = 5000

    postgres_ip = "localhost"
    postgres_port = 5433
    postgres_db = "DemoTesi"
    postgres_user = "postgres"
    postgres_password = "andrea"
