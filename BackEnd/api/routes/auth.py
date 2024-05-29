from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask import session, redirect, request, jsonify
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db.db import get_db

oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/callback',
    client_kwargs={'scope': 'email'}
)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def login():
    return google.authorize_redirect()

def logout():
    session.pop('google_token', None)
    session.pop('user_id', None)
    session.pop('temp_links', None)
    return redirect('/')

def callback():
    token = google.authorize_access_token()
    if token is None or 'access_token' not in token:
        return 'Access denied'

    session['google_token'] = (token['access_token'], '')
    userinfo = google.parse_id_token(token)
    user_data = userinfo.data

    email = user_data.get('email')

    if not email:
        return 'Access denied: Email address not provided by Google.'

    db = get_db()
    cursor = db.cursor()
    
    # Check if user exists
    cursor.execute("SELECT ID FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        # Insert new user
        cursor.execute("INSERT INTO Users (email) VALUES (%s)", (email,))
        db.commit()
        cursor.execute("SELECT ID FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
    
    session['user_id'] = user[0]

    return redirect('/')

def init_app(app):
    app.route('/login')(login)
    app.route('/logout')(logout)
    app.route('/callback')(callback)