from functools import wraps
from flask import session, redirect, url_for, request
import logging
from flask_login import LoginManager, UserMixin, login_required as flask_login_required, logout_user
from requests_oauthlib import OAuth2Session
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db.db import get_db


login_manager = LoginManager()

client_id = GOOGLE_CLIENT_ID
client_secret = GOOGLE_CLIENT_SECRET
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'https://www.pianomusic.com:5000/callback'
scope = ['https://www.googleapis.com/auth/userinfo.profile', 'openid', 'https://www.googleapis.com/auth/userinfo.email']

logging.basicConfig(level=logging.DEBUG)


class User(UserMixin):
    pass

def create_oauth_session(token=None, state=None):
    return OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        token=token,
        state=state,
        scope=scope 
    )


def index():
    if 'google_token' in session:
        google = create_oauth_session(token=session['google_token'])
        user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        return redirect('https://www.pianomusic.com:3000/') 
    return 'You are not logged in<br><a href="/login">Login</a>'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


def login():
    google = create_oauth_session()
    authorization_url, state = google.authorization_url(
        authorization_base_url,
        access_type='offline',
        prompt='select_account'
    )
    session['oauth_state'] = state
    return redirect(authorization_url)

def callback():
    google = create_oauth_session(state=session['oauth_state'])
    token = google.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url
    )
    session['google_token'] = token

    userinfo_response = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    userinfo = userinfo_response.json()

    email = userinfo.get('email')

    if not email:
        return 'Access denied: Email address not provided by Google.'

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id_user FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute("INSERT INTO Users (email) VALUES (%s)", (email,))
        db.commit()
        cursor.execute("SELECT id_user FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()

    session['user_id'] = user[0]

    return redirect('https://www.pianomusic.com:3000/')


@flask_login_required
def logout():
    session.pop('google_token', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.route('/login')(login)
    app.route('/logout')(logout)
    app.route('/callback')(callback)
    app.route('/')(index)

