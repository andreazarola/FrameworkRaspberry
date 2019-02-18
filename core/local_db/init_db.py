import sqlite3
from local_db.setupLamp import setupLamp
from config import Config

def init_db(path):

    absolutePath = path + Config.local_db_name

    conn = sqlite3.connect(absolutePath)

    conn.execute("CREATE TABLE IF NOT EXISTS Dato ("
                 "id integer primary key,"
                 "timestamp text,"
                 "tipo text,"
                 "dato real)")

    conn.execute("CREATE TABLE IF NOT EXISTS Info ("
                 "id_lampione integer primary_key,"
                 "idArea integer,"
                 "latitudine real,"
                 "longitudine real,"
                 "static_ip text,"
                 "prevLamp integer,"
                 "nextLamp integer )")

    conn.execute("CREATE TABLE IF NOT EXISTS Pre_elaborato ("
                 "tipo text,"
                 "giorno text,"
                 "ora integer,"
                 "numCampioni integer,"
                 "valore real,"
                 "timestamp text,"
                 "primary key (tipo, giorno, ora))")

    """timestamp --> si riferisce al timestamp ricevuto, cioè quando e stato generato il timestamp sul server"""
    """timestamp_ricezione --> si riferisce al timestamp di quando e stato l'alert dal listener"""
    conn.execute("CREATE TABLE IF NOT EXISTS Alert ("
                 "id integer primary key autoincrement, "
                 "tipo text,"
                 "valore integer,"
                 "timestamp text,"
                 "timestamp_ricezione text,"
                 "eseguito integer default 0)")

    conn.commit()

    conn.close()

    setupLamp(absolutePath)
