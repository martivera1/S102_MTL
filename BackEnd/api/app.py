from flask import Flask, jsonify
from flask_cors import CORS
from .routes import api_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the API Blueprint
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)