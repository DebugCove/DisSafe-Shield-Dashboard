from os import getenv
from dotenv import load_dotenv

from config.json_handler import load_config


def run_project(app):
    load_dotenv()
    status = load_config()['status']
    DEBUG = getenv('DEBUG')
    HOST = str(getenv('HOST'))

    if status == 'development':
        PORT = getenv('DEVELOPMENT')
        app.run(port=PORT, debug=DEBUG, host=HOST)
    elif status == 'production':
        PORT = getenv('PRODUCTION')
        app.run(port=PORT, debug=DEBUG, host=HOST)
    else:
        raise ValueError('Status inválido')
