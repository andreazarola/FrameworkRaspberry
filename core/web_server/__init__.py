from flask import Flask
from web_server.routes import routes

app = Flask(__name__)

app.register_blueprint(routes)
