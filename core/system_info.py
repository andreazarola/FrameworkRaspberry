"""Classe statica che contiene le informazioni sul lampione"""
"""Va modificata per ogni lampione"""


class SystemInfo:
    """
    :param idLampione: id del lampione all'interno dell'intero sistema
    :param idArea: id dell'area in cui si trova il lampione
    :param lat: latitudine del punto in cui si trova il lampione
    :param lon: longitudine del punto in cui si trova il lampione
    :param prevLamp:
    """

    idLampione = 0
    idArea = 0
    lat = 0
    lon = 0
    static_ip = '192.168.1.22'
    prevLamp = None
    nextLamp = None
