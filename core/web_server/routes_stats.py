from flask import Blueprint
from flask import request
from local_db.dbconnection_factory import DBConnectionFactory
from request.id_sequence import SequenzaId
from flask import json

routes_stats = Blueprint('urls_stats', __name__)


@routes_stats.route('/getStats', methods=['POST'])
def get_stats():
    connection = DBConnectionFactory.create_connection()
    last = SequenzaId.get_instance().get_last()
    limit = 10
    c = connection.cursor()
    c.execute('SELECT tipo FROM Dato GROUP BY tipo')
    result = c.fetchall()
    json_data = {}
    for row in result:
        tipo = row[0]
        c.execute('SELECT tipo, timestamp, dato '
                     'FROM Dato '
                     'WHERE tipo = ? and id <= ? '
                     'ORDER BY id DESC '
                     'LIMIT ?', (tipo, last, limit))
        data_list = list()
        for data in c.fetchall():
            data_list.append({'timestamp': data[1],
                              'valore': data[2]})
        json_data[tipo] = data_list[::-1]
    connection.close()
    r = json.jsonify(json_data)
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r


@routes_stats.route('/getStatsWithLimit', methods=['POST'])
def getStastWithLimit():
    connection = DBConnectionFactory.create_connection()
    last = SequenzaId.get_instance().get_last()
    limit = request.values.get('limit')
    tipo = request.values.get('tipo')
    c = connection.cursor()
    c.execute('SELECT timestamp, dato '
              'FROM Dato '
              'WHERE tipo = ? and id <= ? '
              'ORDER BY id DESC '
              'LIMIT ?', (tipo, last, limit))
    data_list = list()
    for data in c.fetchall():
        data_list.append({'timestamp': data[0],
                          'valore': data[1]})
    json_data = data_list[::-1]
    connection.close()
    r = json.jsonify(json_data)
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r
