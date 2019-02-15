from flask import Blueprint
from flask import request
from flask import make_response
from configuration.configuration_handler import ConfigurationHandler
from flask import json

routes = Blueprint('urls', __name__)


@routes.route('/', methods=['POST', 'GET'])
def index():
    return 'Lamp configuration server'


@routes.route('/getConfiguration', methods=['POST',])
def getConfiguration():
    r = make_response()
    data = ConfigurationHandler.get_instance().get_all()
    json_data = list()
    for d in data:
        json_data.append({'Nome': d.get_nome(),
                    'Tipo': d.get_tipo(),
                    'Valore': d.get_valore()})
    r = json.jsonify(json_data)
    return r
