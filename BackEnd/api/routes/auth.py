from functools import wraps
from flask import session, redirect, url_for, request, jsonify
import logging
from flask_login import LoginManager, UserMixin, login_required as flask_login_required, logout_user
from requests_oauthlib import OAuth2Session
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db.db import get_db
from session import load_session, save_session

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
    session_data = load_session()
    if 'user_id' in session_data:
        return redirect('https://www.pianomusic.com:3000/')
    return 'You are not logged in<br><a href="/login">Login</a>'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_data = load_session()
        if 'user_id' not in session_data:
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
    session_data = load_session()
    session_data['oauth_state'] = state
    save_session(session_data)
    return redirect(authorization_url)

def callback():
    session_data = load_session()
    state = session_data.get('oauth_state')

    if not state:
        return 'Error: oauth_state not found in session'

    google = create_oauth_session(state=state)
    token = google.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url
    )
    session_data['google_token'] = token

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

    session_data['user_id'] = user[0]
    save_session(session_data)  # Save updated session data

    return redirect('https://www.pianomusic.com:3000/')

@login_required
def logout():
    session_data = load_session()
    session_data.pop('google_token', None)
    session_data.pop('user_id', None)
    save_session(session_data)

    response = jsonify({'message': 'Logout successful'})
    response.headers.add('Access-Control-Allow-Origin', 'https://www.pianomusic.com:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    return response

def get_user_info():
    session_data = load_session()
    if 'user_id' in session_data:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT email FROM Users WHERE id_user = %s", (session_data['user_id'],))
        user = cursor.fetchone()
        logging.debug(f"\nuser session: {session_data}")
        if user:
            return jsonify({"email": user[0]})
    return jsonify({"email": None})

def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.add_url_rule('/login', 'login', login, methods=['GET'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET'])
    app.add_url_rule('/callback', 'callback', callback, methods=['GET'])
    app.add_url_rule('/', 'index', index, methods=['GET'])
    app.add_url_rule('/api/user_info', 'get_user_info', get_user_info, methods=['GET'])

    # Load initial session data if any
    session_data = load_session()
    app.config['SESSION_DATA'] = session_data

