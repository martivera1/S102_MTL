from flask_oauthlib.client import OAuth
from functools import wraps
from flask import session, redirect, request, jsonify
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db import get_db

oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET,
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def login():
    return google.authorize(callback='http://localhost:5000/callback')

def logout():
    session.pop('google_token', None)
    session.pop('user_id', None)
    session.pop('temp_links', None)
    return redirect('/')

def callback():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    userinfo = google.get('userinfo')
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

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

def init_app(app):
    app.route('/login')(login)
    app.route('/logout')(logout)
    app.route('/callback')(callback)