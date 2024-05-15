
@app.route('/upload_link', methods=['POST'])
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

@app.route('/modify_link', methods=['PUT'])
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

@app.route('/delete_link', methods=['DELETE'])
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

@app.route('/generate_ranking', methods=['POST'])
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