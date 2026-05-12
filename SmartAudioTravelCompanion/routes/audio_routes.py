import os
from flask import Blueprint, send_from_directory, abort
from config import Config

audio_bp = Blueprint('audio', __name__)


# -------------------------------
# SERVE AUDIO FILES
# -------------------------------
@audio_bp.route('/audio/<path:filename>')
def serve_audio(filename):
    """
    Serve audio files from static/audio folder
    """

    audio_folder = Config.AUDIO_UPLOAD_FOLDER

    # Security check (prevent path traversal)
    file_path = os.path.join(audio_folder, filename)

    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(audio_folder, filename)