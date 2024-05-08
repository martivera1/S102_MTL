from flask import Flask, jsonify, g
import mysql.connector

app = Flask(__name__)

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