from flask import Blueprint
from flask import request
from flask import make_response
from base.lamp_manager import LampManager
from configuration.configuration_handler import ConfigurationHandler
from configuration.configuration_trigger import ConfigurationTrigger
from flask import json
from web_server.user import User

routes = Blueprint('urls', __name__)


@routes.route('/', methods=['POST', 'GET'])
def index():
    return 'Lamp configuration server'


@routes.route('/getConfiguration', methods=['POST'])
def get_configuration():
    status = view_token_status(request)
    if status == 200:
        data = ConfigurationHandler.get_instance().get_all()
        json_data = list()
        for d in data:
            json_data.append({'Nome': d.get_nome(),
                        'Tipo': d.get_tipo(),
                        'Valore': d.get_valore()})
        r = json.jsonify(json_data)
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return response_error_status(status)


@routes.route('/setConfiguration', methods=['POST'])
def setConfiguration():
    status = view_token_status(request)
    if status == 200:
        nome = request.args.get("nome")
        valore = request.args.get("valore")
        ConfigurationHandler.get_instance().set_param(nome, valore)
        ConfigurationHandler.get_instance().save_config()
        r = make_response()
        r.data = "ok"
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return response_error_status(status)


@routes.route('/getTriggerConfiguration', methods=['POST'])
def getTriggerConfiguration():
    status = view_token_status(request)
    if status == 200:
        data = ConfigurationTrigger.get_instance().get_all()
        json_data = list()
        for t in data:
            json_data.append({
                'Trigger': t.get_nome(),
                'Hour': t.get_hour(),
                'Minute': t.get_minute(),
                'Second': t.get_second()})
        r = json.jsonify(json_data)
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return response_error_status(status)


@routes.route('/setTriggerConfiguration', methods=['POST'])
def setTriggerConfiguration():
    status = view_token_status(request)
    if status == 200:
        sensor = request.values.get("trigger")
        second = request.values.get("second")
        minute = request.values.get("minute")
        hour = request.values.get("hour")
        result = ConfigurationTrigger.get_instance().set_trigger(sensor, hour=hour, minute=minute, second=second)
        ConfigurationTrigger.get_instance().save_triggers()
        r = None
        if result is True:
            r = make_response()
            r.data = "ok"
        else:
            r = make_response()
            r.data = "errore nella modifica"
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return response_error_status(status)


@routes.route('/getDefaultAlertValue', methods=['POST'])
def getDefaultAlertValues():
    status = view_token_status(request)
    if status == 200:
        light = LampManager.getInstance().get_valore()
        safety = ConfigurationHandler.get_instance().get_param('livello_sicurezza')
        data = {'led': light, 'safety': safety}
        r = json.jsonify(data)
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return response_error_status(status)


@routes.route('/getToken', methods=['POST'])
def get_token():
    utente = request.values.get("utente")
    password = request.values.get("password")
    try:
        user = User.query(utente, password)
        auth_token = user.encode_auth_token(user.name)
        if auth_token:
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }
            r = make_response(json.jsonify(responseObject))
            r.headers.add('Access-Control-Allow-Origin', '*')
            r.status_code = 200
            return r
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        r = make_response(json.jsonify(responseObject))
        r.headers.add('Access-Control-Allow-Origin', '*')
        r.status_code = 500
        return r


def view_token_status(request):
    auth_header = request.values.get("token")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        return resp
    else:
        """
            Vuol dire che il token inviato non è valido
        """
        return 403


def response_error_status(error):
    resp = None
    if error == 401:
        resp = "Signature expired. Please log in again."
    elif error == 402:
        resp = "Invalid token. Please log in again."
    elif error == 403:
        resp = 'Provide a valid auth token.'
    else:
        resp = 'Unknown error'
    responseObject = {
        'status': 'fail',
        'message': resp
    }
    r = make_response(json.jsonify(responseObject))
    r.headers.add('Access-Control-Allow-Origin', '*')
    r.status_code = 401
    return r
