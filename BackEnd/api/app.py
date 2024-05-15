from flask import Flask, jsonify, g, session, redirect
import mysql.connector
import json
import os
from functools import wraps
from flask_oauthlib.client import OAuth
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from db import get_db, close_db
from routes.auth import login_required, callback
from routes.auth import init_app as init_auth
from routes.ranking import init_app as init_ranking


app = Flask(__name__)

init_auth(app)
init_ranking(app)

app.secret_key = 'pianoclassification_app_key'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

@app.route('/', methods=['GET'])
@login_required
def home():
    return 'Hello, World!'

@login_required
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user():
    print("inside")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE ID = %s", (user_id,))
    user = cursor.fetchall()
    return str(user)  # You might want to format the output more nicely.

@login_required
@app.route('/allrankings', methods=['GET'])
def get_allrankings():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT r.ranking, r.name, r.star, r.description, u.email, o.name
    FROM Ranking r
    JOIN Users u ON r.ID = u.ID
    JOIN Obra o ON r.ID = o.id;
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

@app.route('/obras', methods=['GET'])
@login_required
def get_all_obras():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, epoca, compositor, piano_roll, descriptors, time FROM Obra"
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
            'time': obra[6]
        })
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)