from local_db.dbconnection_factory import DBConnectionFactory
from datetime import datetime
from logs.logger import Logger
import re

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def clean_old_data():
    timestamp = datetime.now()
    conn = DBConnectionFactory.create_connection()
    conn.create_function("REGEXP", 2, regexp)
    today = timestamp.strftime("%A")
    hour = 23
    max_id = None
    giorno = two_day_ago(today)
    clean_old_alert(conn, today, giorno, hour)
    while max_id is None and today != giorno:
        regex = str(giorno) + ",\s\d{2}\.\s[a-zA-Z]+\s\d{4}\s" + str(hour) + ":\d+.+"
        for val in conn.execute("SELECT max(id) "
                                "FROM Dato as d "
                                "WHERE d.timestamp REGEXP \'" + regex + "\'"):
            if val[0] is not None:
                max_id = int(val[0])
        hour -= 1
        if hour < 0:
            hour = 23
            giorno = prec_giorno(giorno)

    if max_id is not None:
        conn.execute('DELETE FROM Dato '
                     'WHERE id <= ?', (max_id,))
        Logger.getInstance().printline("Resettati dati di due giorni fa")

    conn.commit()
    conn.close()


def clean_old_alert(conn, today, giorno, hour):
    max_id = None
    while max_id is None and today != giorno:
        regex = str(giorno) + ",\s\d{2}\.\s[a-zA-Z]+\s\d{4}\s" + str(hour) + ":\d+.+"
        for val in conn.execute("SELECT max(id) "
                                "FROM Alert as a "
                                "WHERE a.timestamp REGEXP \'" + regex + "\'"):
            if val[0] is not None:
                max_id = int(val[0])
        hour -= 1
        if hour < 0:
            hour = 23
            giorno = prec_giorno(giorno)

    if max_id is not None:
        conn.execute('DELETE FROM Alert '
                     'WHERE id <= ?', (max_id,))
        Logger.getInstance().printline("Resettati alert di due giorni fa")


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


def prec_giorno(giorno):
    i = None
    for count, d in enumerate(days):
        if giorno == d:
            i = count
    j = i - 1
    if j < 0:
        j = 7 + j
    return days[j]


def two_day_ago(giorno):
    """
    :param giorno: nome del giorno
    :return: restituisce il nome dei due giorni fa
    """
    i = None
    for count, d in enumerate(days):
        if giorno == d:
            i = count
    j = i - 2
    if j < 0:
        j = 7 + j
    return days[j]
