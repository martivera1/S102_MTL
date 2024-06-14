from flask import jsonify, session, request
from functools import wraps
from db.db import get_db
from routes.auth import login_required
import re

from pytube import YouTube
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
import librosa
import torch
import time
import os
import tempfile

import json
import pretty_midi
import numpy as np
from collections import Counter
from scipy.stats import entropy
import pickle

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
    audio_filename = f"audio_{time.time()}.mp3"
    midi_filename = f"piano_roll_{time.time()}.midi"  #TODO Define same time for both files


    # Download the audio from the YouTube video
    descargar_audio(url, output_path, audio_filename)

    #time.sleep(20)
    #print("5 seconds passed")

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
    loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
    modified_model = loaded_model.partial_fit(
        X_partial_train, y_partial_train, classes=[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10], sample_weight=5000/len(y_partial_train)
    )
    return modified_model

def generate_new_exploration(modified_model, giant_midi_features):
    X = prepare_dataset_giantmidi(giant_midi_features)
    predictions = modified_model.predict(X)
    return {k: int(v) for k, v in zip(giant_midi_features.keys(), predictions)}
######################################################################

# @login_required
def upload_link():
    if request.method == 'POST':
        # Extract JSON data from request body
        print("checkpoint1")
        data = request.json
        print(data)

        # Check if 'link' and 'ranking' are present in the JSON data
        if 'link' in data:
            link = data['link']

            print(f"link: {link}")

            if "youtube" in link:
                pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
                match = re.search(pattern, link)

                ### TESTING DOWNLOAD AND TRANSCRIPTION OF YOUTUBE VIDEO
                youtube_id = match.group(1)
                youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"

                print("checkpoint2")

                audio_path, midi_path = process_youtube_video(youtube_url)

                print("checkpoint3")
                ##############################################

                ### TESTING COMPUTATION OF FEATURES
                pitch_sets = extract_pitch_sets(midi_path)
                complexity = lz_complexity(pitch_sets)
                entropy = compute_pitch_entropy(pitch_sets) 

                features = {
                    'complexity': complexity,
                    'entropy': entropy,
                    'ranking': 1 # TODO ADD RANKING INTO JSON WHEN GENERATING RANKING
                }

                # Check if 'features.json' exists, if not create an empty dictionary
                if os.path.exists('/api/routes/tmp/features.json'):
                    with open('/api/routes/tmp/features.json', 'r') as f:
                        all_features = json.load(f)
                else:
                    all_features = {}

                # Add the features of the current MIDI file to the dictionary
                all_features[youtube_id] = features

                # Write the updated dictionary back to 'features.json'
                with open('/api/routes/tmp/features.json', 'w') as f:
                    json.dump(all_features, f)
                ##############################################

            # elif "imslp" in link:

            if 'temp_links' not in session:
                session['temp_links'] = []

            temp_links = session['temp_links']
            temp_links.append({
                'link': youtube_id,
                'ranking': 1 # TODO ADD RANKING INTO JSON WHEN GENERATING RANKING
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
        INSERT INTO Ranking (name, star, description, user_id, obra_id)
        VALUES (%s, %s, %s, %s)
        """     
        cursor.execute(query, (name, star, description, user_id, obra_id))
        db.commit()

        ### TESTING PARTIAL FIT OF THE MODEL --> charge giantmidi_features.json from the database
        #                                    --> precharge the model or add path of the model finalized_model.sav
        # Load the features of the MIDI files
        with open('features.json', 'r') as f:
            features = json.load(f)

        # Prepare the dataset
        X_partial_train, y_partial_train = prepare_dataset(features)

        # Load the model and perform partial fit
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
        modified_model = loaded_model.partial_fit(
            X_partial_train, y_partial_train, classes=[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10], sample_weight=5000/len(y_partial_train)
        )

        # Generate new exploration
        with open('giantmidi_features.json') as f:
            giant_midi_features = json.load(f)
        exploration_ranking = generate_new_exploration(modified_model, giant_midi_features)

        ##############################################

        return jsonify({'message': 'Ranking generated successfully'})
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
        result.append({
            'ranking': ranking[0],
            'name': ranking[1],
            'star': ranking[2],
            'description': ranking[3],
            'email': ranking[4],
            'obra_name': ranking[5],
        })
    
    return jsonify(result)

# @login_required
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

def init_app(app):
    app.route('/upload_link', methods=['POST'])(upload_link)
    app.route('/modify_link', methods=['PUT'])(modify_link)
    app.route('/delete_link', methods=['DELETE'])(delete_link)
    app.route('/generate_ranking', methods=['POST'])(generate_ranking)
    app.route('/myrankings', methods=['GET'])(get_user_rankings)
    app.route('/allrankings', methods=['GET'])(get_all_rankings)
    app.route('/results', methods=['GET'])(get_results)