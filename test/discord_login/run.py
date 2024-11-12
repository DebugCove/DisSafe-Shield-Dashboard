from os import getenv
from dotenv import load_dotenv
from app.app import create_app

load_dotenv()

config = getenv('FLASK_ENV') or 'development'

app = create_app()

if __name__ == "__main__":
    if config == 'development':
        HOST = getenv('HOST')
        DEBUG = getenv('DEVELOPMENT_DEBUG')
        PORT = getenv('DEVELOPMENT_PORT')
        app.run(host=HOST, debug=DEBUG, port=PORT)
    else:
        HOST = getenv('HOST')
        DEBUG = getenv('PRODUCTION_DEBUG')
        PORT = getenv('PRODUCTION_PORT')
        app.run(host=HOST, debug=DEBUG, port=PORT)
