import sqlite3


def init_db():
    conn = sqlite3.connect("localDB.db")

    conn.execute("CREATE TABLE IF NOT EXISTS Dato ("
                 "timestamp text,"
                 "tipo text,"
                 "dato real,"
                 "primary key(timestamp,tipo))")

    conn.execute("CREATE TABLE IF NOT EXISTS Info ("
                 "id_lampione integer,"
                 "area text,"
                 "latitudine real,"
                 "longitudine real,"
                 "primary key (id_lampione,area))")

    conn.execute("CREATE TABLE IF NOT EXISTS Pre_elaborato ("
                 "tipo text,"
                 "giorno text,"
                 "ora integer,"
                 "valore real,"
                 "timestamp text    ,"
                 "primary key (tipo, giorno, ora))")

    conn.commit()

    conn.close()
