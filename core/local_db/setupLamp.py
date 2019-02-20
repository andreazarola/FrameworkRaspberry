from request.es_connection_factory import ESConnectionFactory
from request.es_request_factory import ES_RequestFactory
from request.HiveConnectionFactory import HiveConnectionFactory
from logs.logger import Logger
from urllib3.exceptions import NewConnectionError as ConnectionError
from config import Config
import sqlite3


def setupLamp(absolutePath):
    conn = sqlite3.connect(absolutePath)

    setted = False

    for row in conn.execute('SELECT * FROM Info'):
        setted = True

    if not setted :
        conn.execute("DELETE FROM Info")
        conn.commit()

        conn.execute("INSERT INTO Info "
            "VALUES (?, ?, ?, ?, ?, ?, ?)", (Config.idLampione, Config.idArea,
                                             Config.lat, Config.lon,
                                             Config.static_ip, Config.prevLamp, Config.nextLamp))
        conn.commit()

        conn.close()

    setup_es()
    setup_hive()


def setup_es():
    try:
        es = ESConnectionFactory().createConnection()
        query = {
            'size': '0',
            'query': {
                'match': {
                    'id_lamp': str(Config.idLampione)
                }
            }
        }
        response = es.search(doc_type='', body=query)
        exists = True if response['hits']['total'] == 1 else False
        if not exists:
            insertLamp(es)
    except (ConnectionError, ConnectionRefusedError):
        Logger.getInstance().printline("Errore durante la comunicazione con ElasticSearch")


def insertLamp(es_conn):
    try:
        conn = es_conn
        req = ES_RequestFactory().createRequest()
        req.initialize().set_connection(conn)
        req.set_index('sensor')
        req.add_param_to_doc('static_ip', Config.static_ip)
        req.add_param_to_doc('id_lamp', str(Config.idLampione))
        req.add_param_to_doc('id_area', str(Config.idArea))
        req.add_param_to_doc('latitude', str(Config.lat))
        req.add_param_to_doc('longitude', str(Config.lon))
        req.execute()
    except (ConnectionError, ConnectionRefusedError):
        Logger.getInstance().printline("Errore durante la comunicazione con ElasticSearch")


def setup_hive():
    try:
        conn = HiveConnectionFactory.create_connection()
        cursor = conn.cursor()
        query = ("select * from lampione where id_lampione = " + str(Config.idLampione))
        cursor.execute(query)
        result_set = cursor.fetchall()
        exist = False
        if len(result_set) > 0:
            exist = True
        if not exist:
            insert_lamp_on_hive(cursor)
        conn.close()
    except Exception as e:
        Logger.getInstance().printline(str(e) + '\n' + "on setup_hive")


def insert_lamp_on_hive(cursor):
    insert = ("insert into table lampione values (" + str(Config.idLampione) + ", " + str(Config.idArea) + ", " +
                                                str(Config.lat) + ", " + str(Config.lon) + ", " +
                                                "'" + Config.static_ip + "')")
    cursor.execute(insert)
