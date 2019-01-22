from request.es_connection_factory import ESConnectionFactory
from request.es_request_factory import ES_RequestFactory
import sqlite3

"""
parametri di identificazione del lampione
"""
idLamp = 0
idArea = 0
lat = 39.2915
lon = 16.256195
static_ip = 'localhost'
""" prevLamp = None -> è il primo lampione dell'area """
""" nextLamp = None -> è l'ultimo lampione dell'area """
prevLamp = None
nextLamp = None


def setupLamp(absolutePath):
    conn = sqlite3.connect(absolutePath)

    setted = False

    for row in conn.execute('SELECT * FROM Info'):
        setted = True

    if not setted :
        conn.execute("DELETE FROM Info")
        conn.commit()

        conn.execute("INSERT INTO Info "
            "VALUES (?, ?, ?, ?, ?, ?, ?)", (idLamp, idArea, lat, lon, static_ip, prevLamp, nextLamp))
        conn.commit()

        conn.close()

    setup_es()


def setup_es():
    es = ESConnectionFactory().createConnection()
    query = {
        'size': '0',
        'query': {
            'match': {
                'id_lamp': str(idLamp)
            }
        }
    }
    response = es.search(doc_type='', body=query)
    exists = True if response['hits']['total'] == 1 else False
    if not exists:
        insertLamp(es)


def insertLamp(es_conn):
    conn = es_conn
    req = ES_RequestFactory().createRequest()
    req.initialize().set_connection(conn)
    req.set_index('sensor')
    req.add_param_to_doc('static_ip', static_ip)
    req.add_param_to_doc('id_lamp', str(idLamp))
    req.add_param_to_doc('id_area', str(idArea))
    req.add_param_to_doc('latitude', str(lat))
    req.add_param_to_doc('longitude', str(lon))
    req.execute()
