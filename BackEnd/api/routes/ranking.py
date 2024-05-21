from flask import jsonify, session, request
from functools import wraps
from db import get_db
from routes.auth import login_required

@login_required
def upload_link():
    if request.method == 'POST':
        
        link = request.args.get('link')
        ranking = request.args.get('ranking')
        
        if 'temp_links' not in session:
            session['temp_links'] = []

        temp_links = session['temp_links']
        temp_links.append({
            'link': link,
            'ranking': ranking
        })
        session['temp_links'] = temp_links

        return 'Link submitted successfully'
    else:
        return 'There was an error uploading the link'

@login_required
def modify_link():
    if request.method == 'PUT':
        old_link = request.args.get('old_link')
        new_link = request.args.get('new_link')
        new_ranking = request.args.get('new_ranking')

        if 'temp_links' not in session:
            return jsonify({'error': 'No links to modify'}), 404

        temp_links = session['temp_links']
        for item in temp_links:
            if item['link'] == old_link:
                item['link'] = new_link
                if new_ranking:
                    item['ranking'] = new_ranking
                break
        session['temp_links'] = temp_links

        return jsonify({'message': 'Link modified successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@login_required
def delete_link():
    if request.method == 'DELETE':
        old_link = request.args.get('old_link')
        
        if 'temp_links' not in session:
            return jsonify({'error': 'No links to delete'}), 404

        temp_links = session['temp_links']
        temp_links = [item for item in temp_links if item['link'] != old_link]
        session['temp_links'] = temp_links

        return jsonify({'message': 'Link deleted successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@login_required
def generate_ranking():
    if request.method == 'POST':
        
        # logic to generate the ranking with temp_links
        if 'temp_links' not in session:
            return jsonify({'error': 'No links to generate ranking'}), 404

        temp_links = session['temp_links']

        data = request.get_json()
        ranking = data.get('ranking')
        name = data.get('name')

        star = data.get('star')
        description = data.get('description')
        user_id = data.get('user_id')
        obra_id = data.get('obra_id')
        
        db = get_db()
        cursor = db.cursor()
        
        query = """
        INSERT INTO Ranking (name, star, description, user_id, obra_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, star, description, user_id, obra_id))
        db.commit()

        return jsonify({'message': 'Ranking generated succesfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@login_required
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

def init_app(app):
    app.route('/upload_link', methods=['POST'])(upload_link)
    app.route('/modify_link', methods=['PUT'])(modify_link)
    app.route('/delete_link', methods=['DELETE'])(delete_link)
    app.route('/generate_ranking', methods=['POST'])(generate_ranking)
    app.route('/allrankings', methods=['GET'])(get_allrankings)