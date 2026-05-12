from database.models.playback_session import PlaybackSession
from database.models.listening_history import ListeningHistory
from database.models.usage_report import UsageReport
from database.models.audio_story import AudioStory

from services.recommendation_service import RecommendationService


class TrackingService:

    # -------------------------------
    # START TRACKING (WHEN PLAY STARTS)
    # -------------------------------
    @staticmethod
    def start_tracking(user_id, story_id):
        """
        Initialize tracking when playback starts
        """

        # Ensure listening history exists
        ListeningHistory.get_or_create(user_id, story_id)

        # Increment play count
        UsageReport.get_or_create(story_id)
        UsageReport.increment_play_count(story_id)

    # -------------------------------
    # TRACK LISTENING TIME (PAUSE/STOP)
    # -------------------------------
    @staticmethod
    def track_listening(user_id, time_spent):
        """
        Update listening time when user pauses/stops
        """

        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return

        ListeningHistory.update_listening_time(
            user_id,
            session.story_id,
            time_spent
        )

    # -------------------------------
    # TRACK SKIP
    # -------------------------------
    @staticmethod
    def track_skip(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return

        ListeningHistory.increment_skip(user_id, session.story_id)

    # -------------------------------
    # TRACK REPLAY
    # -------------------------------
    @staticmethod
    def track_replay(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return

        ListeningHistory.increment_replay(user_id, session.story_id)

    # -------------------------------
    # TRACK COMPLETION
    # -------------------------------
    @staticmethod
    def track_completion(user_id):
        session = PlaybackSession.get_by_user(user_id)

        if not session:
            return

        # Mark completed
        ListeningHistory.mark_completed(user_id, session.story_id)

        # Update engagement
        UsageReport.update_engagement_rate(session.story_id)

    # -------------------------------
    # END SESSION (FINALIZE TRACKING)
    # -------------------------------
    @staticmethod
    def end_session(user_id):
        """
        Called when session ends → updates AI preferences
        """

        # Update user preferences based on full session
        RecommendationService.update_user_preferences(user_id)

    # -------------------------------
    # GET USER HISTORY (FOR UI)
    # -------------------------------
    @staticmethod
    def get_user_history(user_id):
        history = ListeningHistory.get_user_history(user_id)

        result = []
        for record in history:
            story = AudioStory.get_by_id(record.story_id)

            result.append({
                "story": story.to_dict() if story else None,
                "listening_time": record.listening_time,
                "skip_count": record.skip_count,
                "replay_count": record.replay_count,
                "completed": record.completion_status
            })

        return result

    # -------------------------------
    # CLEAR USER HISTORY
    # -------------------------------
    @staticmethod
    def clear_history(user_id):
        ListeningHistory.clear_user_history(user_id)