from flask import Blueprint
from flask import request
from flask import make_response
from base.lamp_manager import LampManager
from configuration.configuration_handler import ConfigurationHandler
from configuration.configuration_trigger import ConfigurationTrigger
from flask import json

routes = Blueprint('urls', __name__)


@routes.route('/', methods=['POST', 'GET'])
def index():
    return 'Lamp configuration server'


@routes.route('/getConfiguration', methods=['POST',])
def get_configuration():
    data = ConfigurationHandler.get_instance().get_all()
    json_data = list()
    for d in data:
        json_data.append({'Nome': d.get_nome(),
                    'Tipo': d.get_tipo(),
                    'Valore': d.get_valore()})
    r = json.jsonify(json_data)
    return r


@routes.route('/setConfiguration', methods=['POST'])
def setConfiguration():
    nome = request.args.get("nome")
    valore = request.args.get("valore")
    ConfigurationHandler.get_instance().set_param(nome, valore)
    print(nome + valore)
    r = make_response()
    r.data = "ok"
    return r


@routes.route('/getTriggerConfiguration', methods=['POST'])
def getTriggerConfiguration():
    data = ConfigurationTrigger.get_instance().get_all()
    json_data = list()
    for t in data:
        json_data.append({
            'Trigger': t.get_nome(),
            'Hour': t.get_hour(),
            'Minute': t.get_minute(),
            'Second': t.get_second()})
    r = json.jsonify(json_data)
    return r


@routes.route('/setTriggerConfiguration', methods=['POST'])
def setTriggerConfiguration():
    sensor = request.values.get("trigger")
    second = request.values.get("second")
    minute = request.values.get("minute")
    hour = request.values.get("hour")
    result = ConfigurationTrigger.get_instance().set_trigger(sensor, hour=hour, minute=minute, second=second)
    r = None
    if result is True:
        r = make_response()
        r.data = "ok"
    else:
        r = make_response()
        r.data = "errore nella modifica"
    return r


@routes.route('/getDefaultAlertValue', methods=['POST'])
def getDefaultAlertValues():
    light = LampManager.getInstance().get_valore()
    safety = ConfigurationHandler.get_instance().get_param('livello_sicurezza')
    data = {'led': light, 'safety': safety}
    r = json.jsonify(data)
    return r

