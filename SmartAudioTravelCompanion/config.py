import os

class Config:
    # Base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Instance folder (for database)
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

    # Ensure instance folder exists
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    # SQLite database path
    DATABASE_PATH = os.path.join(INSTANCE_DIR, 'database.db')

    # Flask secret key (change this in real deployment)
    SECRET_KEY = 'dev_secret_key_12345'

    # Debug mode
    DEBUG = True

    # Audio upload folder
    AUDIO_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'audio')

    # Ensure audio folder exists
    if not os.path.exists(AUDIO_UPLOAD_FOLDER):
        os.makedirs(AUDIO_UPLOAD_FOLDER)

    # Allowed audio file types
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}