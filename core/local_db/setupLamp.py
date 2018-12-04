import sqlite3

"""
parametri di identificazione del lampione
"""
idLamp = 0
area = "Piazza Crispi"
lat = 39.2915
lon = 16.256195

conn = sqlite3.connect("localDB.db")

conn.execute("DELETE FROM Info")
conn.commit()

conn.execute("INSERT INTO Info "
             "VALUES (?, ? ,? ,?)", (idLamp, area, lat, lon))
conn.commit()

conn.close()
