from os import urandom
from flask import Flask
from flask_session import Session
from app.initialize_functions import initialize_route, initialize_swagger

def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = urandom(36)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    initialize_route(app)
    initialize_swagger(app)

    return app
