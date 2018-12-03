import sqlite3

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

conn.commit()

conn.close()