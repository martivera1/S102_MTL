from flask import jsonify, session, request
from functools import wraps
from db.db import get_db
from routes.auth import login_required
import re
import threading

from pytube import YouTube
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
import librosa
import torch
import time
import os
import tempfile
import logging

import json
import pretty_midi
import numpy as np
from collections import Counter
from scipy.stats import entropy
import pickle
from sklearn.impute import SimpleImputer
import uuid

### CODE TO DOWNLOAND VIDEO AND EXTRACT AUDIO AND TRANSCRIBE IT TO MIDI
def process_youtube_video(url):
    output_path = "/api/routes/tmp/"
    def descargar_audio(url, output_path, filename):
        try:

            youtube = YouTube(url);
            video= youtube.streams.filter(only_audio=True).first();
            video.download(output_path=output_path, filename=filename);
        except:
            print("File not downloaded correctly")

    # Generate unique filenames
    unique_id = time.time()
    audio_filename = f"audio_{unique_id}.mp3"
    midi_filename = f"piano_roll_{unique_id}.midi"  


    # Download the audio from the YouTube video
    descargar_audio(url, output_path, audio_filename)


    # Load audio
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu");
    audio_path = os.path.join(output_path, audio_filename)

    os.chmod(audio_path, 0o777)


    while not os.path.exists(audio_path):
        print("Waiting for file to be written to disk...")
        time.sleep(1)

    print("File exists, proceeding...")

    #(audio, _) = librosa.load(audio_path, sr=sample_rate, mono=True);
    (audio, _) = librosa.core.load(audio_path, sr=sample_rate, mono=True);
    #(audio, ) = load_audio(audio_path, sr=sample_rate, mono=True)

    # Transcriptor
    print('Pre transcriptor', flush=True)
    transcriptor = PianoTranscription(device=device)

    # Transcribe and write out to MIDI file
    midi_path = os.path.join(output_path, midi_filename)
    print('Start transcriptor', flush=True)
    transcribed_dict = transcriptor.transcribe(audio, midi_path)
    os.chmod(midi_path, 0o777)

    return audio_path, midi_path
######################################################################  

### CODE TO COMPUTE THE FEATURES OF THE MIDI FILE
TIME_THRESHOLD = 0.05  # Adjust this value as needed

def extract_pitch_sets(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    pitch_sets = []

    # Combine notes into simultaneous events
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            current_event = []
            current_start_time = None
            for note in instrument.notes:
                if current_start_time is None or note.start <= current_start_time + TIME_THRESHOLD:
                    current_event.append(note.pitch)
                    current_start_time = min(current_start_time, note.start) if current_start_time is not None else note.start
                else:
                    pitch_sets.append('-'.join(map(str, sorted(current_event))))
                    current_event = [note.pitch]
                    current_start_time = note.start
            if current_event:
                pitch_sets.append('-'.join(map(str, sorted(current_event))))

    return pitch_sets


def lz_complexity(s):
    p = 0
    C = 1
    u = 1
    v = 1
    vmax = v
    while u + v < len(s):
        if s[p - 1 + v] == s[u + v - 1]:
            v += 1
        else:
            vmax = max(v, vmax)
            p += 1
            if p == u:
                C += 1
                u += vmax
                v = 1
                p = 0
                vmax = v
            else:
                v = 1
    if v > 1:
        C += 1
    return C


def compute_pitch_entropy(pitch_sets):
    pitch_counts = Counter(pitch_sets)
    probabilities = np.array(list(pitch_counts.values())) / len(pitch_sets)
    return entropy(probabilities)
######################################################################

### CODE TO DO PARTIAL FIT OF THE MODEL
def prepare_dataset(data):
    features = []
    labels = []
    for item in data:
        features.append([
            item['complexity'],
            item['entropy']
        ])
        labels.append(item['grade'])
    return np.array(features), np.array(labels)

def prepare_dataset_giantmidi(data):
    features = []
    for item in data.values():
        features.append([
            item['complexity'],
            item['entropy']
        ])
    return np.array(features)

def partial_fit(new_data):
    X_partial_train, y_partial_train = prepare_dataset(new_data)
    loaded_model = pickle.load(open("/api/routes/finalized_model.sav", 'rb'))
    modified_model = loaded_model.partial_fit(
        X_partial_train, y_partial_train, classes=[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10], sample_weight=7000/len(y_partial_train)
    )
    return modified_model

def generate_new_exploration(modified_model, giant_midi_features):
    #X = prepare_dataset_giantmidi(giant_midi_features)
    predictions = modified_model.predict(giant_midi_features)
    return predictions

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    new_data = []
    for youtube_id, features in data.items():
        new_data.append({
            'complexity': features['complexity'],
            'entropy': features['entropy'],
            'grade': features['grade']
        })

    return new_data
######################################################################

# @login_required
def process_link(link, youtube_id):
    audio_path, midi_path = process_youtube_video(link)
    pitch_sets = extract_pitch_sets(midi_path)
    complexity = lz_complexity(pitch_sets)
    entropy_value = compute_pitch_entropy(pitch_sets)
    
    features = {
        'complexity': complexity,
        'entropy': entropy_value
    }

    # Guardar las características en features.json
    if os.path.exists('/api/routes/tmp/features.json'):
        with open('/api/routes/tmp/features.json', 'r') as f:
            all_features = json.load(f)
    else:
        all_features = {}

    all_features[youtube_id] = features

    with open('/api/routes/tmp/features.json', 'w') as f:
        json.dump(all_features, f)

    # Eliminar archivos temporales
    os.remove(audio_path)
    os.remove(midi_path)

    # Actualizar estado a 'finished' en status.json
    if os.path.exists('/api/routes/tmp/status.json'):
        with open('/api/routes/tmp/status.json', 'r') as f:
            status_dict = json.load(f)
    else:
        status_dict = {}

    status_dict[link] = 'finished'

    with open('/api/routes/tmp/status.json', 'w') as f:
        json.dump(status_dict, f)

### Lógica para subir un enlace
def upload_link():
    if request.method == 'POST':
        data = request.json
        if 'link' in data:
            link = data['link']

            if "youtube" in link:
                pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
                match = re.search(pattern, link)

                if match:
                    youtube_id = match.group(1)

                    if 'temp_links' not in session:
                        session['temp_links'] = []

                    temp_links = session['temp_links']
                    temp_links.append({
                        'link': youtube_id
                    })
                    session['temp_links'] = temp_links

                    # Process link synchronously
                    process_link(link, youtube_id)

                    return jsonify({'message': 'Enlace está siendo procesado', 'link': youtube_id, 'status': 'completed'}), 202

                else:
                    return jsonify({"error": "Enlace de YouTube inválido"}), 400
            else:
                return jsonify({"error": "Formato de enlace inválido"}), 400
        else:
            return jsonify({"error": "Falta 'link' en los datos de la solicitud"}), 400

    return 'Sólo se admite el método POST para este punto final', 405

# @login_required
def modify_link():
    if request.method == 'PUT':
        # Extract JSON data from request body
        data = request.json

        print(data)

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

# @login_required
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
        # Check if 'links' is present in the request
        data = request.json

        if 'links' not in data:
            
            return jsonify({'error': 'No links to generate ranking'}), 404

        # Extract required parameters from JSON data
        name = data.get('name')
        star = data.get('star')
        description = data.get('description')
        user_id = data.get('user')

        # Insert the ranking into the database
        #db = get_db()
        #cursor = db.cursor()
        #query = """
        #INSERT INTO Ranking (name, star, description, user_id, obra_id)
        #VALUES (%s, %s, %s, %s)
        #"""     
        #cursor.execute(query, (name, star, description, user_id, obra_id))
        #db.commit()

        ### TESTING PARTIAL FIT OF THE MODEL 
        links= data['links']

        pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'

        # Load the features of the MIDI files
        with open('/api/routes/tmp/features.json', 'r') as f:
            all_features = json.load(f)

        for link_data in links:
            link = link_data['link']
            grade = link_data['grade']
            match = re.search(pattern, link)
            if match:
                youtube_id = match.group(1)

                # If the youtube_id is already in all_features, update it with the grade
                if youtube_id in all_features:
                    all_features[youtube_id]['grade'] = grade
                else:
                    # If the youtube_id is not in all_features, add it with the grade
                    all_features[youtube_id] = {'grade': grade}

        # Write the updated dictionary back to 'features.json'
        with open('/api/routes/tmp/features.json', 'w') as f:
            json.dump(all_features, f)

        new_data = load_data('/api/routes/tmp/features.json')

        # Prepare the dataset
        modified_model = partial_fit(new_data)

        #TEST IMPORTING FEATURES FROM JSON FILE
        #with open('giantmidi_features.json') as f: 
        #    giant_midi_features = json.load(f)
        #exploration_ranking = generate_new_exploration(modified_model, giant_midi_features)

        #TEST IMPORTING FEATURES FROM DATABASE (HAURIEM DE FER SERVIR AIXO PER ANAR BÉ), PERO SINO FUNCIONA TIREM DE JSON A LA GUARRA
        db= get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_obra, atr_complexity, atr_entropy FROM Obra where atr_complexity is not null and atr_entropy is not null;")     
        results = cursor.fetchall()

        # Separate the song identifiers and features
        song_ids = [row[0] for row in results]
        features = np.array([row[1:] for row in results])

        # Generate predictions
        predictions = generate_new_exploration(modified_model, features)

        # Create a dictionary with song identifiers and predictions
        song_predictions = {song_id: int(prediction) for song_id, prediction in zip(song_ids, predictions)}

        # Generate a unique ranking_id
        random_uuid_int = uuid.uuid4().int
        ranking_id = (random_uuid_int % 1000) + 1

        # Prepare the SQL query
        sql_query = """
        INSERT INTO Ranking (id_ranking, name, star, description, user_id, obra_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Loop through the song_predictions dictionary
        for song_id, prediction in song_predictions.items():
            # Execute the query
            cursor.execute(sql_query, (ranking_id, name, prediction, description, 14, song_id))

        # Commit the changes
        db.commit()
        
        #After generating the new exploration, delete the features.json file
        os.remove('/api/routes/tmp/features.json')

        ##############################################

        return jsonify({'message': 'Ranking generated successfully',
            'ranking_id': ranking_id}), 200
    
    else:
        return jsonify({'error': 'Method not allowed'}), 405


# @login_required
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
        youtube_id = ranking[6]
        video_name = get_youtube_video_name(youtube_id)

        result.append({
            'ranking': ranking[0],
            'name': video_name,
            'star': ranking[2],
            'description': ranking[3],
            'email': ranking[4],
            'obra_name': ranking[5],
        })
    
    return jsonify(result)

def get_youtube_video_name(video_id):
    try:
        return f'https://www.youtube.com/watch?v={video_id}'
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Unknown Title"

# @login_required
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

def get_rankings():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT 
        r.id_ranking, 
        MAX(r.name) as name, 
        MAX(r.star) as star, 
        MAX(r.description) as description, 
        MAX(u.email) as username
    FROM 
        Ranking r
    LEFT JOIN 
        Users u ON r.user_id = u.id_user
    GROUP BY 
        r.id_ranking;
    """
    cursor.execute(query)
    rankings = cursor.fetchall()

    result = []
    for ranking in rankings:
        result.append({
            'id': ranking[0],
            'name': ranking[1] if ranking[1] else "",
            'star': ranking[2],
            'description': ranking[3] if ranking[3] else "",
            'username': ranking[4] if ranking[4] else "Unknown"
        })
    
    return jsonify(result)

def get_ranking_results(ranking_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch up to 10 obras per star level for the given ranking_id
    query = """
    SELECT o.id_obra, o.name, o.epoca, o.compositor, o.piano_roll, o.atr_complexity, o.atr_entropy, o.atr_duration, o.time, r.star
    FROM Obra o
    JOIN Ranking r ON o.id_obra = r.obra_id
    WHERE r.id_ranking = %s
    ORDER BY r.star DESC, o.id_obra
    """
    cursor.execute(query, (ranking_id,))
    obras = cursor.fetchall()

    result = {}
    for obra in obras:
        star_level = obra[9]  # Assuming 'star' column index in Ranking table is 9 (adjust if needed)
        if star_level <= 10:  # Only include star levels from 1 to 10
            if star_level not in result:
                result[star_level] = []
            if len(result[star_level]) < 10:  # Limit to 10 obras per star level
                name = get_youtube_video_name(obra[1])
                result[star_level].append({
                    'id_obra': obra[0],
                    'name': name,
                    'epoca': obra[2],
                    'compositor': obra[3],
                    'piano_roll': obra[4],
                    'atr_complexity': obra[5],
                    'atr_entropy': obra[6],
                    'atr_duration': obra[7],
                    'time': obra[8]
                })

    return jsonify(result)


def get_links():
    return jsonify([])

def init_app(app):
    app.route('/upload_link', methods=['POST'])(upload_link)
    app.route('/modify_link', methods=['PUT'])(modify_link)
    app.route('/delete_link', methods=['DELETE'])(delete_link)
    app.route('/generate_ranking', methods=['POST'])(generate_ranking)
    app.route('/myrankings', methods=['GET'])(get_user_rankings)
    app.route('/results', methods=['GET'])(get_results)
    app.route('/get_links', methods=['GET'])(get_links)
    app.route('/get_rankings', methods=['GET'])(get_rankings)
    app.route('/get_ranking_results/<int:ranking_id>', methods=['GET'])(get_ranking_results)
    