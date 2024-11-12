from os import getenv
from flask import Flask
from flasgger import Swagger
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from app.modules.main.route import main_bp

oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='discord',
        client_id=getenv('DISCORD_CLIENT_ID'),
        client_secret=getenv('DISCORD_CLIENT_SECRET'),
        access_token_url='https://discord.com/api/oauth2/token',
        authorize_url='https://discord.com/api/oauth2/authorize',
        api_base_url='https://discord.com/api/',
        client_kwargs={'scope': 'identify', 'state': True},
    )

    Session(app) 

def initialize_route(app: Flask):
    with app.app_context():
        init_oauth(app)
        app.register_blueprint(main_bp, url_prefix='/')

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger
