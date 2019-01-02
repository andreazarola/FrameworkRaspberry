import sqlite3

"""
parametri di identificazione del lampione
"""
idLamp = 0
area = "Piazza Crispi"
idArea = 0
lat = 39.2915
lon = 16.256195
""" prevLamp = None -> è il primo lampione dell'area """
""" nextLamp = None -> è l'ultimo lampione dell'area """
prevLamp = None
nextLamp = 1

conn = sqlite3.connect("localDB.db")

conn.execute("DELETE FROM Info")
conn.commit()

conn.execute("INSERT INTO Info "
             "VALUES (?, ? ,?, ?, ?, ?, ?)", (idLamp, area, idArea, lat, lon, prevLamp, nextLamp))
conn.commit()

conn.close()
