import os
from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db_pg = False
if db_pg:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bac_rest"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db?timeout=60')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes

db.create_all()

if not os.environ.get("WERKZEUG_RUN_MAIN"):
    from src.bacnet_server.mqtt_connection import MqttConnection
    from src.bacnet_server.bac_server import BACServer

    mqtt_thread = Thread(target=MqttConnection.start, daemon=True)
    mqtt_thread.start()
    BACServer.get_instance().start_bac()
