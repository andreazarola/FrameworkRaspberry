import sqlite3

conn = sqlite3.connect("localDB.db")

conn.execute("CREATE TABLE IF NOT EXISTS Dato ("
             "timestamp text,"
             "tipo text,"
             "dato real,"
             "primary key(timestamp,tipo))")

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
             "timestamp text,"
             "timestamp_ricezione text,"
             "eseguito integer default 0)")

conn.commit()

conn.close()
