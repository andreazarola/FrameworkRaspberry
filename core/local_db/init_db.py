import sqlite3

def init_db(path):
    conn = sqlite3.connect(path + "localDB.db")

    conn.execute("CREATE TABLE IF NOT EXISTS Dato ("
                 "timestamp text,"
                 "tipo text,"
                 "dato real,"
                 "primary key(timestamp,tipo))")

    conn.execute("CREATE TABLE IF NOT EXISTS Info ("
                 "id_lampione integer primary_key,"
                 "area text,"
                 "idArea integer,"
                 "latitudine real,"
                 "longitudine real,"
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

    conn.commit()

    conn.close()
