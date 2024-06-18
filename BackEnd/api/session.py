import json
from pathlib import Path

DEFAULT_SESSION = {
    'user_id': None,
    'username': 'guest',
    'permissions': [],
    # Add more default session data as needed
}

SESSION_FILE = 'session.json'

def load_session():
    try:
        with open('/api/sessions/session.json', 'r') as f:
            session_data = json.load(f)
    except FileNotFoundError:
        print("Session file not found. Using default session.")
        session_data = DEFAULT_SESSION
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}. Using default session.")
        session_data = DEFAULT_SESSION

    return session_data

def save_session(session_data):
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)
