from flask import Flask
from web_server.routes import routes
from web_server.routes_stats import routes_stats

app = Flask(__name__)

app.register_blueprint(routes)
app.register_blueprint(routes_stats)
