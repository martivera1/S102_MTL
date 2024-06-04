import os
# Define Google OAuth Client ID and Client Secret
GOOGLE_CLIENT_ID = '942443179924-1fudpksmoi2kh69igqg4ao1nvjv5qk6s.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '$\x14\x03#Rxa6\xc0\x90j\xd7p\t}\xc3r\xa3_\x11\xa6\xcd;\xff')
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/api/sessions'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True