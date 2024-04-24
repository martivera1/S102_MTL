from flask import Blueprint, jsonify

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/home', methods=['GET', 'POST'])
def home():
    return jsonify({'message': 'Homepage!'})

@api_bp.route('/upload', methods=['POST'])
def upload():
    return jsonify({'message': 'Page for uploading.'})
