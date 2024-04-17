from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve():
    return send_from_directory(os.path.join(os.getcwd(), 'frontend', 'build'), 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.getcwd(), 'frontend', 'build', 'static'), path)

if __name__ == '__main__':
    app.run(debug=True)
