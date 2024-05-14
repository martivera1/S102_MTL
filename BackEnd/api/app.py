from flask import Flask, jsonify, g, session, redirect
import mysql.connector
import json
import os
from functools import wraps
from flask_oauthlib.client import OAuth
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

temp_links = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_token' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/', methods=['GET'])
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

@app.route('/upload_link', methods=['POST'])
def upload_link():
    if request.method == 'POST':
        
        link = request.args.get('link')
        ranking = request.args.get('ranking')
        
        temp_links.append({
            'link': link,
            'ranking': ranking
        })

        return 'Link submitted successfully'
    else:
        return 'There was an error uploading the link'

@app.route('/modify_link', methods=['PUT'])
def modify_link():
    if request.method == 'PUT':
        old_link = request.args.get('old_link')
        new_link = request.args.get('new_link')
        new_ranking = request.args.get('new_ranking')

        for item in temp_links:
            if item['link'] == old_link:
                item['link'] = new_link
                if (ranking):
                    item['ranking'] = new_ranking

        return jsonify({'message': 'Link modified successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/delete_link', methods=['DELETE'])
def delete_link():
    if request.method == 'DELETE':
        old_link = request.args.get('old_link')
        
        for item in temp_links:
            if item['link'] == old_link:
                temp_links.pop(item)

        return jsonify({'message': 'Link deleted successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/generate_ranking', methods=['POST'])
def delete_link():
    if request.method == 'POST':
        

        return jsonify({'message': 'Ranking generated succesfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405




@app.route('/login')
def login():
    return google.authorize(callback='http://localhost:5000/callback')

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    # session.clear()
    return redirect('/')

@app.route('/callback')
def callback():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    userinfo = google.get('userinfo')
    return jsonify(userinfo.data)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)