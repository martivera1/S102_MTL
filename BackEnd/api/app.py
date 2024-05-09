from flask import Flask, jsonify, g
import mysql.connector
import json
from functools import wraps
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

app = Flask(__name__)
app.secret_key = 'pianoclassification_app_key'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

oauth = OAuth(app)
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


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="pianoclassification"
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()
        del g.db

@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/users/<int:user_id>')
def get_user():
    print("inside")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE ID = %s", (user_id,))
    user = cursor.fetchall()
    return str(user)  # You might want to format the output more nicely.

@app.route('/allrankings')
def get_allrankings():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT ID, email FROM users")
    users = cursor.fetchall()
    print(users)
    return str(users)  # You might want to format the output more nicely.



if __name__ == '__main__':
    app.run(debug=True)
