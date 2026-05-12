import os
from config import Config

from database.models.audio_story import AudioStory
from database.models.playback_session import PlaybackSession
from database.models.listening_history import ListeningHistory
from database.models.usage_report import UsageReport


class AudioService:

    # -------------------------------
    # GET ALL STORIES
    # -------------------------------
    @staticmethod
    def get_all_stories():
        return [story.to_dict() for story in AudioStory.get_all_stories()]

    # -------------------------------
    # GET STORY BY ID
    # -------------------------------
    @staticmethod
    def get_story(story_id):
        story = AudioStory.get_by_id(story_id)
        return story.to_dict() if story else None

    # -------------------------------
    # START PLAYBACK
    # -------------------------------
    @staticmethod
    def start_playback(user_id, story_id):
        """
        Start a new playback session
        """

        # Create playback session
        PlaybackSession.create_session(user_id, story_id)

        # Track play count
        UsageReport.get_or_create(story_id)
        UsageReport.increment_play_count(story_id)

        # Ensure history record exists
        ListeningHistory.get_or_create(user_id, story_id)

        return {"success": True, "message": "Playback started"}

    # -------------------------------
    # PAUSE PLAYBACK
    # -------------------------------
    @staticmethod
    def pause_playback(user_id, position):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No active session"}

        PlaybackSession.pause(session.session_id, position)

        # Track listening time
        ListeningHistory.update_listening_time(user_id, session.story_id, position)

        return {"success": True, "message": "Playback paused"}

    # -------------------------------
    # RESUME PLAYBACK
    # -------------------------------
    @staticmethod
    def resume_playback(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No session found"}

        PlaybackSession.resume(session.session_id)

        return {
            "success": True,
            "message": "Playback resumed",
            "position": session.current_position
        }

    # -------------------------------
    # STOP PLAYBACK
    # -------------------------------
    @staticmethod
    def stop_playback(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No session found"}

        PlaybackSession.stop(session.session_id)

        return {"success": True, "message": "Playback stopped"}

    # -------------------------------
    # SKIP STORY
    # -------------------------------
    @staticmethod
    def skip_story(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No session found"}

        ListeningHistory.increment_skip(user_id, session.story_id)

        PlaybackSession.stop(session.session_id)

        return {"success": True, "message": "Story skipped"}

    # -------------------------------
    # REPLAY STORY
    # -------------------------------
    @staticmethod
    def replay_story(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No session found"}

        ListeningHistory.increment_replay(user_id, session.story_id)

        # Restart playback
        PlaybackSession.update_position(session.session_id, 0)
        PlaybackSession.resume(session.session_id)

        return {"success": True, "message": "Story replayed"}

    # -------------------------------
    # COMPLETE STORY
    # -------------------------------
    @staticmethod
    def complete_story(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return {"success": False, "message": "No session found"}

        # Mark complete
        ListeningHistory.mark_completed(user_id, session.story_id)

        # Update engagement rate
        UsageReport.update_engagement_rate(session.story_id)

        PlaybackSession.stop(session.session_id)

        return {"success": True, "message": "Story completed"}

    # -------------------------------
    # GET AUDIO FILE PATH
    # -------------------------------
    @staticmethod
    def get_audio_file_path(story_id):
        story = AudioStory.get_by_id(story_id)

        if not story:
            return None

        return story.file_path

    # -------------------------------
    # UPLOAD AUDIO FILE (ADMIN)
    # -------------------------------
    @staticmethod
    def save_audio_file(file):
        """
        Save uploaded file to static/audio
        """
        if not file:
            return None

        filename = file.filename

        # Validate extension
        if '.' not in filename or filename.split('.')[-1].lower() not in Config.ALLOWED_AUDIO_EXTENSIONS:
            return None

        filepath = os.path.join(Config.AUDIO_UPLOAD_FOLDER, filename)

        file.save(filepath)

        # Return relative path for DB
        return f"static/audio/{filename}"