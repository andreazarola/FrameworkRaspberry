from flask import Blueprint
from local_db.dbconnection_factory import DBConnectionFactory
from request.id_sequence import SequenzaId
from flask import json

routes_stats = Blueprint('urls_stats', __name__)


@routes_stats.route('/getStats', methods=['POST'])
def get_stats():
    connection = DBConnectionFactory.create_connection()
    last = SequenzaId.get_instance().get_last()
    limit = 40
    c = connection.cursor()
    c.execute('SELECT timestamp, tipo, dato '
              'FROM Dato '
              'WHERE id <= ? and id > ?'
              'ORDER BY id ASC ', (last, last-limit))
    data_list = c.fetchall()
    print(data_list)
    json_data = {}
    for row in data_list:
        if row[1] not in json_data:
            json_data[row[1]] = list()
        json_data[row[1]].append({'timestamp': row[0],
                                  'valore': row[2]})
    r = json.jsonify(json_data)
    return r

