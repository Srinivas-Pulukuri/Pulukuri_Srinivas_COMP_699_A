from database.db import execute_query


class PlaybackSession:
    def __init__(self, session_id=None, user_id=None, story_id=None, current_position=0, status='stopped'):
        self.session_id = session_id
        self.user_id = user_id
        self.story_id = story_id
        self.current_position = current_position
        self.status = status  # playing, paused, stopped

    # -------------------------------
    # CREATE NEW SESSION (START PLAY)
    # -------------------------------
    @staticmethod
    def create_session(user_id, story_id):
        query = """
            INSERT INTO playback_session (user_id, story_id, current_position, status)
            VALUES (?, ?, ?, ?)
        """
        execute_query(query, (user_id, story_id, 0, 'playing'), commit=True)

    # -------------------------------
    # GET ACTIVE SESSION BY USER
    # -------------------------------
    @staticmethod
    def get_by_user(user_id):
        query = """
            SELECT * FROM playback_session
            WHERE user_id = ?
            ORDER BY session_id DESC LIMIT 1
        """
        row = execute_query(query, (user_id,), fetch_one=True)

        if row:
            return PlaybackSession(
                session_id=row["session_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                current_position=row["current_position"],
                status=row["status"]
            )
        return None

    # -------------------------------
    # UPDATE CURRENT POSITION
    # -------------------------------
    @staticmethod
    def update_position(session_id, position):
        query = """
            UPDATE playback_session
            SET current_position = ?
            WHERE session_id = ?
        """
        execute_query(query, (position, session_id), commit=True)

    # -------------------------------
    # PAUSE SESSION
    # -------------------------------
    @staticmethod
    def pause(session_id, position):
        query = """
            UPDATE playback_session
            SET current_position = ?, status = 'paused'
            WHERE session_id = ?
        """
        execute_query(query, (position, session_id), commit=True)

    # -------------------------------
    # RESUME SESSION
    # -------------------------------
    @staticmethod
    def resume(session_id):
        query = """
            UPDATE playback_session
            SET status = 'playing'
            WHERE session_id = ?
        """
        execute_query(query, (session_id,), commit=True)

    # -------------------------------
    # STOP SESSION
    # -------------------------------
    @staticmethod
    def stop(session_id):
        query = """
            UPDATE playback_session
            SET status = 'stopped', current_position = 0
            WHERE session_id = ?
        """
        execute_query(query, (session_id,), commit=True)

    # -------------------------------
    # DELETE SESSION (CLEANUP)
    # -------------------------------
    @staticmethod
    def delete_session(session_id):
        query = """
            DELETE FROM playback_session WHERE session_id = ?
        """
        execute_query(query, (session_id,), commit=True)

    # -------------------------------
    # GET ALL SESSIONS (ADMIN DEBUG)
    # -------------------------------
    @staticmethod
    def get_all_sessions():
        query = "SELECT * FROM playback_session"
        rows = execute_query(query, fetch_all=True)

        sessions = []
        for row in rows:
            sessions.append(PlaybackSession(
                session_id=row["session_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                current_position=row["current_position"],
                status=row["status"]
            ))
        return sessions

    # -------------------------------
    # CONVERT OBJECT TO DICT
    # -------------------------------
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "story_id": self.story_id,
            "current_position": self.current_position,
            "status": self.status
        }