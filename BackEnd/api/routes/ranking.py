from flask import jsonify, session, request
from functools import wraps
from db.db import get_db
from routes.auth import login_required

# @login_required
def upload_link():
    if request.method == 'POST':
        # Extract JSON data from request body
        data = request.json
        
        # Check if 'link' and 'ranking' are present in the JSON data
        if 'link' in data and 'ranking' in data:
            link = data['link']
            ranking = data['ranking']

            print(f"link: {link}, ranking: {ranking}")

            if "youtube" in link:
                pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
                match = re.search(pattern, link)
                link = match.group(1)

            # elif "imslp" in link:

            if 'temp_links' not in session:
                session['temp_links'] = []

            temp_links = session['temp_links']
            temp_links.append({
                'link': youtube_id,
                'ranking': ranking
            })
            session['temp_links'] = temp_links

            print(session['temp_links'])

            return 'Link submitted successfully'
        else:
            return 'Invalid JSON data: "link" and "ranking" fields are required', 400
    else:
        return 'Only POST method is supported for this endpoint', 405

# @login_required
def modify_link():
    if request.method == 'PUT':
        # Extract JSON data from request body
        data = request.json

        # Check if 'old_link' and 'new_link' are present in the JSON data
        if 'old_link' in data and 'new_link' in data:
            old_link = data['old_link']
            new_link = data['new_link']
            new_ranking = data.get('new_ranking')  # Optional parameter
            
            if 'temp_links' not in session:
                return jsonify({'error': 'No links to modify'}), 404

            temp_links = session['temp_links']
            link_modified = False
            for item in temp_links:
                if item['link'] == old_link:
                    item['link'] = new_link
                    if new_ranking:
                        item['ranking'] = new_ranking
                    link_modified = True
                    break
            
            if link_modified:
                session['temp_links'] = temp_links
                return jsonify({'message': 'Link modified successfully'})
            else:
                return jsonify({'error': 'Old link not found'}), 404

        else:
            return jsonify({'error': 'Missing required fields: "old_link" and "new_link"'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@login_required
def delete_link():
    if request.method == 'DELETE':
        # Extract JSON data from request body
        data = request.json

        # Check if 'old_link' is present in the JSON data
        if 'old_link' in data:
            old_link = data['old_link']
            
            if 'temp_links' not in session:
                return jsonify({'error': 'No links to delete'}), 404

            temp_links = session['temp_links']
            temp_links = [item for item in temp_links if item['link'] != old_link]
            session['temp_links'] = temp_links

            return jsonify({'message': 'Link deleted successfully'})
        else:
            return jsonify({'error': 'Missing required field: "old_link"'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

# @login_required
def generate_ranking():
    if request.method == 'POST':
        # Check if 'temp_links' is present in the session
        if 'temp_links' not in session:
            return jsonify({'error': 'No links to generate ranking'}), 404

        # Extract JSON data from request body
        data = request.json

        # Extract required parameters from JSON data
        name = data.get('name')
        star = data.get('star')
        description = data.get('description')
        user_id = session.get('user_id')

        # Insert the ranking into the database
        db = get_db()
        cursor = db.cursor()
        query = """
        INSERT INTO Ranking (name, star, description, ID)
        VALUES (%s, %s, %s, %s)
        """     
        cursor.execute(query, (name, star, description, user_id))
        db.commit()

        

        return jsonify({'message': 'Ranking generated successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@login_required
def get_user_rankings():

    user_id = session.get('user_id')

    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT r.ranking, r.name, r.star, r.description, u.email, o.name
    FROM Ranking r
    JOIN Users u ON r.ID = u.ID
    JOIN Obra o ON r.ID = o.id
    WHERE u.ID = %s;
    """
    cursor.execute(query, (user_id,))
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

@login_required
def get_all_rankings():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT r.ranking, r.name, r.star, r.description, u.email, o.name
    FROM Ranking r
    JOIN Users u ON r.ID = u.ID
    JOIN Obra o ON r.ID = o.id
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

@login_required
def get_results():

    user_id = session.get('user_id')

    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT r.ranking, r.name, r.star, r.description, u.email, o.name
    FROM Ranking r
    JOIN Users u ON r.ID = u.ID
    JOIN Obra o ON r.ID = o.id
    WHERE u.ID = %s
    """
    cursor.execute(query, (user_id,))
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
    app.route('/myrankings', methods=['GET'])(get_user_rankings)
    app.route('/allrankings', methods=['GET'])(get_all_rankings)
    app.route('/results', methods=['GET'])(get_results)