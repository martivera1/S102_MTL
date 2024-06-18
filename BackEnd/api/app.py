from flask import Flask, jsonify, g, session, redirect
from flask_session import Session
import mysql.connector
import json
import os
import sys
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask_login import LoginManager

from db.db import get_db, close_db
from routes.auth import init_app as init_auth
from routes.ranking import init_app as init_ranking
from routes.users import init_app as init_users
from routes.auth import login_required

app = Flask(__name__, static_folder='../Frontend/front-end/build', static_url_path='/')
app.secret_key = 'pianoclassification'
CORS(app, resources={r"/*": {"origins": "https://www.pianomusic.com:3000", "supports_credentials": True}})

# Configure session to use file system (JSON) storage
app.config.from_mapping(
    SESSION_TYPE='filesystem',
    SESSION_FILE_DIR=os.path.join(app.instance_path, 'sessions'),
    SESSION_FILE_THRESHOLD=100,
)

# Ensure the session directory exists
if not os.path.exists(app.config['SESSION_FILE_DIR']):
    os.makedirs(app.config['SESSION_FILE_DIR'])

# Load configuration from the config file
app.config.from_object('config.Config')

Session(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize blueprints or other app components
init_auth(app)
init_ranking(app)
init_users(app)

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pytube').setLevel(logging.WARNING)

@app.route('/home', methods=['GET'])
# @login_required
def home():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT r.id_ranking, r.name, r.star, r.description, u.email, o.name
    FROM Ranking r
    JOIN Users u ON r.id_ranking = u.id_user
    JOIN Obra o ON r.id_ranking = o.id_obra
    """
    cursor.execute(query)
    rankings = cursor.fetchall()

    result = []
    for ranking in rankings:
        result.append({
            'ranking': ranking[0],
            'name': ranking[1],
            'star': ranking[2],
            'description': ranking[3],
            'email': ranking[4],
            'obra_name': ranking[5],
        })
    
    return jsonify(result)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['GET'])
# @login_required
def upload():
    print("upload page")
    return jsonify({'message': 'Upload Page'})

@app.route('/obras', methods=['GET'])
# @login_required
def get_all_obras():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id_obra AS id_obra, name AS name, epoca AS epoca, compositor AS compositor, piano_roll AS piano_roll, atr_complexity AS complexity, atr_entropy AS entropy, atr_duration AS duration, time AS time FROM Obra"
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
            'complexity': obra[5], 
            'entropy': obra[6], 
            'duration': obra[7],
            'time': obra[8] 
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        ssl_context=("cert/pianomusic.com.crt", "cert/pianomusic.com.key"),
        debug=False,
    )
