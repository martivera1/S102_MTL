from flask import Flask, jsonify, g, session, redirect
from flask_session import Session
import mysql.connector
import json
import os
import sys
import logging
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix

from db.db import get_db, close_db
from routes.auth import login_required, callback
from routes.auth import init_app as init_auth
from routes.ranking import init_app as init_ranking
from routes.users import init_app as init_users

app = Flask(__name__)

# Load configuration from the config file
app.config.from_object('config.Config')

Session(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize blueprints or other app components
init_auth(app)
init_ranking(app)
init_users(app)

# app.secret_key = 'pianoclassification_app_key'

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
# @login_required
def home():
    return 'Hello, World!'

@app.route('/obras', methods=['GET'])
# @login_required
def get_all_obras():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id_obra, name, epoca, compositor, piano_roll, descriptor, complexity, entropy, duration, time FROM Obra"
    cursor.execute(query)
    obras = cursor.fetchall()

    result = []
    for obra in obras:
        result.append({
            'id': obra[0],
            'name': obra[1],
            'epoca': obra[2],
            'compositor': obra[3],
            'piano_roll': obra[4],
            'descriptors': obra[5],
            'complexity': obra[6],
            'entropy': obra[7],
            'duration': obra[8],
            'time': obra[9]
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)