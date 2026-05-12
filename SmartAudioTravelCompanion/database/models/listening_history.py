from database.db import execute_query


class ListeningHistory:
    def __init__(self, history_id=None, user_id=None, story_id=None,
                 listening_time=0, skip_count=0, replay_count=0, completion_status=0):
        self.history_id = history_id
        self.user_id = user_id
        self.story_id = story_id
        self.listening_time = listening_time
        self.skip_count = skip_count
        self.replay_count = replay_count
        self.completion_status = completion_status  # 0 = not completed, 1 = completed

    # -------------------------------
    # CREATE OR GET EXISTING RECORD
    # -------------------------------
    @staticmethod
    def get_or_create(user_id, story_id):
        query = """
            SELECT * FROM listening_history
            WHERE user_id = ? AND story_id = ?
        """
        row = execute_query(query, (user_id, story_id), fetch_one=True)

        if row:
            return ListeningHistory(
                history_id=row["history_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                listening_time=row["listening_time"],
                skip_count=row["skip_count"],
                replay_count=row["replay_count"],
                completion_status=row["completion_status"]
            )

        # Create new record if not exists
        insert_query = """
            INSERT INTO listening_history
            (user_id, story_id, listening_time, skip_count, replay_count, completion_status)
            VALUES (?, ?, 0, 0, 0, 0)
        """
        execute_query(insert_query, (user_id, story_id), commit=True)

        return ListeningHistory.get_or_create(user_id, story_id)

    # -------------------------------
    # UPDATE LISTENING TIME
    # -------------------------------
    @staticmethod
    def update_listening_time(user_id, story_id, time_spent):
        query = """
            UPDATE listening_history
            SET listening_time = listening_time + ?
            WHERE user_id = ? AND story_id = ?
        """
        execute_query(query, (time_spent, user_id, story_id), commit=True)

    # -------------------------------
    # INCREMENT SKIP COUNT
    # -------------------------------
    @staticmethod
    def increment_skip(user_id, story_id):
        query = """
            UPDATE listening_history
            SET skip_count = skip_count + 1
            WHERE user_id = ? AND story_id = ?
        """
        execute_query(query, (user_id, story_id), commit=True)

    # -------------------------------
    # INCREMENT REPLAY COUNT
    # -------------------------------
    @staticmethod
    def increment_replay(user_id, story_id):
        query = """
            UPDATE listening_history
            SET replay_count = replay_count + 1
            WHERE user_id = ? AND story_id = ?
        """
        execute_query(query, (user_id, story_id), commit=True)

    # -------------------------------
    # MARK STORY AS COMPLETED
    # -------------------------------
    @staticmethod
    def mark_completed(user_id, story_id):
        query = """
            UPDATE listening_history
            SET completion_status = 1
            WHERE user_id = ? AND story_id = ?
        """
        execute_query(query, (user_id, story_id), commit=True)

    # -------------------------------
    # GET USER HISTORY
    # -------------------------------
    @staticmethod
    def get_user_history(user_id):
        query = """
            SELECT * FROM listening_history WHERE user_id = ?
        """
        rows = execute_query(query, (user_id,), fetch_all=True)

        history_list = []
        for row in rows:
            history_list.append(ListeningHistory(
                history_id=row["history_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                listening_time=row["listening_time"],
                skip_count=row["skip_count"],
                replay_count=row["replay_count"],
                completion_status=row["completion_status"]
            ))
        return history_list

    # -------------------------------
    # CLEAR USER HISTORY
    # -------------------------------
    @staticmethod
    def clear_user_history(user_id):
        query = """
            DELETE FROM listening_history WHERE user_id = ?
        """
        execute_query(query, (user_id,), commit=True)

    # -------------------------------
    # GET ALL HISTORY (ADMIN USE)
    # -------------------------------
    @staticmethod
    def get_all_history():
        query = "SELECT * FROM listening_history"
        rows = execute_query(query, fetch_all=True)

        history_list = []
        for row in rows:
            history_list.append(ListeningHistory(
                history_id=row["history_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                listening_time=row["listening_time"],
                skip_count=row["skip_count"],
                replay_count=row["replay_count"],
                completion_status=row["completion_status"]
            ))
        return history_list

    # -------------------------------
    # CONVERT TO ML FEATURES
    # -------------------------------
    def to_feature_vector(self):
        """
        Converts user behavior into ML input format
        """
        return [
            self.listening_time,
            self.skip_count,
            self.replay_count,
            self.completion_status
        ]

    # -------------------------------
    # CONVERT OBJECT TO DICT
    # -------------------------------
    def to_dict(self):
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "story_id": self.story_id,
            "listening_time": self.listening_time,
            "skip_count": self.skip_count,
            "replay_count": self.replay_count,
            "completion_status": self.completion_status
        }