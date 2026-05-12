from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from routes.auth_routes import login_required

from services.audio_service import AudioService
from services.recommendation_service import RecommendationService
from services.tracking_service import TrackingService

user_bp = Blueprint('user', __name__)


# -------------------------------
# USER DASHBOARD
# -------------------------------
@user_bp.route('/dashboard')
@login_required(role='traveller')
def dashboard():
    user_id = session.get('user_id')

    # Get personalized recommendations
    stories = RecommendationService.get_recommendations(user_id)

    return render_template('dashboard.html', stories=stories)


# -------------------------------
# PLAY STORY PAGE
# -------------------------------
@user_bp.route('/player/<int:story_id>')
@login_required(role='traveller')
def player(story_id):
    story = AudioService.get_story(story_id)

    if not story:
        flash("Story not found", "danger")
        return redirect(url_for('user.dashboard'))

    return render_template('player.html', story=story)


# -------------------------------
# START PLAYBACK
# -------------------------------
@user_bp.route('/play/<int:story_id>', methods=['POST'])
@login_required(role='traveller')
def play(story_id):
    user_id = session.get('user_id')

    AudioService.start_playback(user_id, story_id)
    TrackingService.start_tracking(user_id, story_id)

    return redirect(url_for('user.player', story_id=story_id))


# -------------------------------
# PAUSE PLAYBACK
# -------------------------------
@user_bp.route('/pause', methods=['POST'])
@login_required(role='traveller')
def pause():
    user_id = session.get('user_id')
    position = float(request.form.get('position', 0))

    AudioService.pause_playback(user_id, position)
    TrackingService.track_listening(user_id, position)

    flash("Playback paused", "info")
    return redirect(url_for('user.dashboard'))


# -------------------------------
# RESUME PLAYBACK
# -------------------------------
@user_bp.route('/resume', methods=['POST'])
@login_required(role='traveller')
def resume():
    user_id = session.get('user_id')

    AudioService.resume_playback(user_id)

    flash("Playback resumed", "info")
    return redirect(url_for('user.dashboard'))


# -------------------------------
# SKIP STORY
# -------------------------------
@user_bp.route('/skip', methods=['POST'])
@login_required(role='traveller')
def skip():
    user_id = session.get('user_id')

    AudioService.skip_story(user_id)
    TrackingService.track_skip(user_id)

    flash("Story skipped", "warning")
    return redirect(url_for('user.dashboard'))


# -------------------------------
# REPLAY STORY
# -------------------------------
@user_bp.route('/replay', methods=['POST'])
@login_required(role='traveller')
def replay():
    user_id = session.get('user_id')

    AudioService.replay_story(user_id)
    TrackingService.track_replay(user_id)

    flash("Story replayed", "info")
    return redirect(url_for('user.dashboard'))


# -------------------------------
# COMPLETE STORY
# -------------------------------
@user_bp.route('/complete', methods=['POST'])
@login_required(role='traveller')
def complete():
    user_id = session.get('user_id')

    AudioService.complete_story(user_id)
    TrackingService.track_completion(user_id)
    TrackingService.end_session(user_id)

    flash("Story completed", "success")
    return redirect(url_for('user.dashboard'))


# -------------------------------
# VIEW HISTORY
# -------------------------------
@user_bp.route('/history')
@login_required(role='traveller')
def history():
    user_id = session.get('user_id')

    history_data = TrackingService.get_user_history(user_id)

    return render_template('history.html', history=history_data)


# -------------------------------
# CLEAR HISTORY
# -------------------------------
@user_bp.route('/clear_history', methods=['POST'])
@login_required(role='traveller')
def clear_history():
    user_id = session.get('user_id')

    TrackingService.clear_history(user_id)

    flash("History cleared", "success")
    return redirect(url_for('user.history'))