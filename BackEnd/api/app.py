from flask import Flask, jsonify, g
import mysql.connector

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
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

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/users/<int:user_id>')
def get_user():
    print("inside")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE ID = %s", (user_id,))
    user = cursor.fetchall()
    return str(user)  # You might want to format the output more nicely.