from local_db.dbconnection_factory import DBConnectionFactory
from datetime import datetime
from logs.logger import Logger
import re


def clean_old_data():
    timestamp = datetime.now()
    giorno = timestamp.strftime("%A")
    hour = 23
    conn = DBConnectionFactory.create_connection()
    re = str(two_day_ago(giorno)) + ",\s\d{2}\.\s[a-zA-Z]+\s\d{4}\s" + str(hour) + ":\d+.+"
    conn.create_function("REGEXP", 2, regexp)

    max_id = None

    for val in conn.execute("SELECT max(id) "
                            "FROM Dato as d "
                            "WHERE timestamp"
                            "WHERE d.timestamp REGEXP \'" + re + "\'"):
        if val[0] is not None:
            max_id = int(val[0])

    if max_id is not None:
        conn.execute('DELETE FROM Dato '
                     'WHERE id <= ?', (id,))
        Logger.getInstance().printline("Resettati dati di due giorni fa")

    conn.commit()
    conn.close()


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


def two_day_ago(giorno):
    """
    :param giorno: nome del giorno
    :return: restituisce il nome dei due giorni fa
    """
    if giorno == "Monday":
        return "Saturday"
    elif giorno == "Tuesday":
        return "Sunday"
    elif giorno == "Wednesday":
        return "Monday"
    elif giorno == "Thursday":
        return "Tuesday"
    elif giorno == "Friday":
        return "Wednesday"
    elif giorno == "Saturday":
        return "Thursday"
    elif giorno == "Sunday":
        return "Friday"
