from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask import session, redirect, request, jsonify
import logging
from uuid import uuid4

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db.db import get_db


# Create OAuth object
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
    redirect_response = google.authorize_redirect()
    logging.debug(f"Generated state: {session.get('_google_authlib_state_')}")
    return redirect_response

    # Generate a new UUID for the state
    new_state = str(uuid4())
    # Store the generated state in the session
    session['_google_authlib_state_'] = new_state
    # Redirect to the authorization URL with the generated state
    return google.authorize_redirect(state=new_state)

def logout():
    session.pop('google_token', None)
    session.pop('user_id', None)
    session.pop('temp_links', None)
    return redirect('/')

def callback():
    logging.debug(f"Request state: {request.args.get('state')}")
    logging.debug(f"Session state: {session.get('_google_authlib_state_')}")

    if session.get('_google_authlib_state_') != request.args.get('state'):
        return 'State mismatch', 400

    token = google.authorize_access_token()
    if token is None or 'access_token' not in token:
        return 'Access denied'

    logging.debug(f"Received token: {token}")

    session['google_token'] = (token['access_token'], '')
    userinfo = google.parse_id_token(token)
    user_data = userinfo.data

    email = user_data.get('email')

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
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
    
    session['user_id'] = user[0]

    return redirect('/')

def init_app(app):
    # Initialize OAuth with Flask app
    oauth.init_app(app)

    app.route('/login')(login)
    app.route('/logout')(logout)
    app.route('/callback')(callback)