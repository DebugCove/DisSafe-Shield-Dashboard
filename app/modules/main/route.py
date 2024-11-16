from flask import Blueprint, render_template, session, url_for, redirect


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    user = session.get('user')
    if user:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/login')
def login():
    from app.initialize_functions import oauth
    redirect_uri = url_for('main.callback', _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)

@main_bp.route('/callback')
def callback():
    from app.initialize_functions import oauth
    token = oauth.discord.authorize_access_token()
    user = oauth.discord.get('users/@me').json()

    avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png" \
        if user.get('avatar') else f"https://cdn.discordapp.com/embed/avatars/{int(user['discriminator']) % 5}.png"

    session['user'] = {
        'id': user['id'],
        'username': user['username'],
        'discriminator': user['discriminator'],
        'avatar_url': avatar_url
    }
    return redirect(url_for('main.dashboard'))


@main_bp.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html', user=user)

@main_bp.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('main.login'))
    return render_template('profile.html', user=user)

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))
