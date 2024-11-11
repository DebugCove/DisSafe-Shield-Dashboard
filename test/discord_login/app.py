from dotenv import load_dotenv
from os import getenv, urandom
from flask import Flask, redirect, url_for, session, render_template
from flask_session import Session
from authlib.integrations.flask_client import OAuth

from config.json_handler import load_config


app = Flask(__name__)
app.secret_key = urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


oauth = OAuth(app)
CLIENT_ID = getenv('DISCORD_CLIENT_ID')
CLIENT_SECRET = getenv('DISCORD_CLIENT_SECRET')
discord = oauth.register(
    name='discord',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize',
    api_base_url='https://discord.com/api/',
    client_kwargs={'scope': 'identify', 'state': True},
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return discord.authorize_redirect(redirect_uri=url_for('callback', _external=True))


@app.route('/callback')
def callback():
    token = discord.authorize_access_token()
    user = discord.get('users/@me').json()
    session['user'] = user
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('login')

    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



if __name__ == "__main__":
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
