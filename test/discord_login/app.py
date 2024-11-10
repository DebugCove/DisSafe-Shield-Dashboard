from os import getenv, urandom
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = urandom(24)


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
    client_kwargs={
        'scope': 'identify',
    },
)


@app.route('/')
def home():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    return render_template('index.html')


@app.route('/login')
def login():
    return discord.authorize_redirect(redirect_uri=url_for('callback', _external=True))


@app.route('/callback')
def callback():
    token = discord.authorize_access_token()
    user = discord.get('users/@me').json()
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3003)
