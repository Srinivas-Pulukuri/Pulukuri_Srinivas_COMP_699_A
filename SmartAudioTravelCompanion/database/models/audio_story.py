from database.db import execute_query


class AudioStory:
    def __init__(self, story_id=None, title=None, category=None, duration=0, file_path=None):
        self.story_id = story_id
        self.title = title
        self.category = category
        self.duration = duration
        self.file_path = file_path

    # -------------------------------
    # CREATE AUDIO STORY (ADMIN)
    # -------------------------------
    @staticmethod
    def create_story(title, category, duration, file_path):
        query = """
            INSERT INTO audio_story (title, category, duration, file_path)
            VALUES (?, ?, ?, ?)
        """
        execute_query(query, (title, category, duration, file_path), commit=True)

    # -------------------------------
    # GET STORY BY ID
    # -------------------------------
    @staticmethod
    def get_by_id(story_id):
        query = """
            SELECT * FROM audio_story WHERE story_id = ?
        """
        row = execute_query(query, (story_id,), fetch_one=True)

        if row:
            return AudioStory(
                story_id=row["story_id"],
                title=row["title"],
                category=row["category"],
                duration=row["duration"],
                file_path=row["file_path"]
            )
        return None

    # -------------------------------
    # GET ALL STORIES
    # -------------------------------
    @staticmethod
    def get_all_stories():
        query = "SELECT * FROM audio_story"
        rows = execute_query(query, fetch_all=True)

        stories = []
        for row in rows:
            stories.append(AudioStory(
                story_id=row["story_id"],
                title=row["title"],
                category=row["category"],
                duration=row["duration"],
                file_path=row["file_path"]
            ))
        return stories

    # -------------------------------
    # GET STORIES BY CATEGORY
    # -------------------------------
    @staticmethod
    def get_by_category(category):
        query = """
            SELECT * FROM audio_story WHERE category = ?
        """
        rows = execute_query(query, (category,), fetch_all=True)

        stories = []
        for row in rows:
            stories.append(AudioStory(
                story_id=row["story_id"],
                title=row["title"],
                category=row["category"],
                duration=row["duration"],
                file_path=row["file_path"]
            ))
        return stories

    # -------------------------------
    # UPDATE STORY DETAILS
    # -------------------------------
    @staticmethod
    def update_story(story_id, title, category, duration):
        query = """
            UPDATE audio_story
            SET title = ?, category = ?, duration = ?
            WHERE story_id = ?
        """
        execute_query(query, (title, category, duration, story_id), commit=True)

    # -------------------------------
    # UPDATE FILE PATH (IF RE-UPLOADED)
    # -------------------------------
    @staticmethod
    def update_file_path(story_id, file_path):
        query = """
            UPDATE audio_story
            SET file_path = ?
            WHERE story_id = ?
        """
        execute_query(query, (file_path, story_id), commit=True)

    # -------------------------------
    # DELETE STORY
    # -------------------------------
    @staticmethod
    def delete_story(story_id):
        query = """
            DELETE FROM audio_story WHERE story_id = ?
        """
        execute_query(query, (story_id,), commit=True)

    # -------------------------------
    # SEARCH STORIES (OPTIONAL)
    # -------------------------------
    @staticmethod
    def search_by_title(keyword):
        query = """
            SELECT * FROM audio_story WHERE title LIKE ?
        """
        rows = execute_query(query, (f"%{keyword}%",), fetch_all=True)

        stories = []
        for row in rows:
            stories.append(AudioStory(
                story_id=row["story_id"],
                title=row["title"],
                category=row["category"],
                duration=row["duration"],
                file_path=row["file_path"]
            ))
        return stories

    # -------------------------------
    # CONVERT OBJECT TO DICT
    # -------------------------------
    def to_dict(self):
        return {
            "story_id": self.story_id,
            "title": self.title,
            "category": self.category,
            "duration": self.duration,
            "file_path": self.file_path
        }