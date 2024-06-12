from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask import session, redirect, request, url_for
from uuid import uuid4
import logging
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db.db import get_db

# Flask-Login setup
login_manager = LoginManager()

# Create OAuth object
oauth = OAuth()

# OAuth configuration
client_id = GOOGLE_CLIENT_ID
client_secret = GOOGLE_CLIENT_SECRET
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'http://localhost:5000/callback'
scope = ['profile', 'email']

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class User(UserMixin):
    pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

def index():
    if 'google_token' in session:
        user_info = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        return f'Logged in as {user_info["email"]}<br><a href="/logout">Logout</a>'
    return 'You are not logged in<br><a href="/login">Login</a>'

def login():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')
    session['oauth_state'] = state
    return redirect(authorization_url)

def callback():
    google = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['google_token'] = token

    userinfo = token['userinfo']
    email = userinfo.get('email')

    if not email:
        return 'Access denied: Email address not provided by Google.'

    db = get_db()
    cursor = db.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id_users FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        # Insert new user
        cursor.execute("INSERT INTO Users (email) VALUES (%s)", (email,))
        db.commit()
        cursor.execute("SELECT id_users FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
    
    session['user_id'] = user[0]

    return redirect('/')

@login_required
def logout():
    session.pop('google_token', None)
    return redirect(url_for('.index'))

def init_app(app):
    # Initialize OAuth with Flask app
    oauth.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.route('/login')(login)
    app.route('/logout')(logout)
    app.route('/callback')(callback)
