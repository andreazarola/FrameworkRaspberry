from request.es_connection_factory import ESConnectionFactory
from request.es_request_factory import ES_RequestFactory
from request.HiveConnectionFactory import HiveConnectionFactory
from logs.logger import Logger
from urllib3.exceptions import NewConnectionError as ConnectionError
from system_info import SystemInfo
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
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (SystemInfo.idLampione, SystemInfo.idArea,
                                                SystemInfo.lat, SystemInfo.lon,
                                                SystemInfo.public_static_ip, SystemInfo.private_static_ip,
                                                SystemInfo.prevLamp, SystemInfo.nextLamp))
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
                    'id_lamp': str(SystemInfo.idLampione)
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
        req.set_index('lampione')
        req.add_param_to_doc('static_ip', SystemInfo.public_static_ip)
        req.add_param_to_doc('alert_port', str(SystemInfo.public_alert_port))
        req.add_param_to_doc('web_server_port', str(SystemInfo.public_web_server_port))
        req.add_param_to_doc('id_lamp', str(SystemInfo.idLampione))
        req.add_param_to_doc('id_area', str(SystemInfo.idArea))
        req.add_param_to_doc('latitude', str(SystemInfo.lat))
        req.add_param_to_doc('longitude', str(SystemInfo.lon))
        req.execute()
    except (ConnectionError, ConnectionRefusedError):
        Logger.getInstance().printline("Errore durante la comunicazione con ElasticSearch")


def setup_hive():
    try:
        conn = HiveConnectionFactory.create_connection()
        cursor = conn.cursor()
        query = ("select * from lampione where id_lampione = " + str(SystemInfo.idLampione))
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
    insert = ("insert into table lampione values (" + str(SystemInfo.idLampione) + ", " + str(SystemInfo.idArea) + ", " +
                                                str(SystemInfo.lat) + ", " + str(SystemInfo.lon) + ", " +
                                                "'" + SystemInfo.public_static_ip + "'," +
                                                str(SystemInfo.public_alert_port) + ", " +
                                                str(SystemInfo.public_web_server_port) + ")")
    cursor.execute(insert)
