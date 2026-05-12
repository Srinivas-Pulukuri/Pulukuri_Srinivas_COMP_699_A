import sqlite3
from config import Config

# Global connection (optional reuse)
connection = None


def get_db_connection():
    """
    Create and return a database connection.
    """
    global connection

    if connection is None:
        connection = sqlite3.connect(Config.DATABASE_PATH, check_same_thread=False)
        connection.row_factory = sqlite3.Row  # Allows dict-like access

    return connection


def close_db_connection():
    """
    Close the database connection.
    """
    global connection

    if connection:
        connection.close()
        connection = None


def init_db():
    """
    Initialize database and create all required tables.
    This runs only once when app starts.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # -------------------------------
    # USER TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'traveller'
        )
    """)

    # -------------------------------
    # TRAVELLER TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traveller (
            traveller_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            interest_profile TEXT,
            privacy_setting TEXT,
            FOREIGN KEY(user_id) REFERENCES user(user_id)
        )
    """)

    # -------------------------------
    # ADMIN TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            FOREIGN KEY(user_id) REFERENCES user(user_id)
        )
    """)

    # -------------------------------
    # AUDIO STORY TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_story (
            story_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            duration REAL,
            file_path TEXT
        )
    """)

    # -------------------------------
    # PLAYBACK SESSION TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playback_session (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            story_id INTEGER,
            current_position REAL DEFAULT 0,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(story_id) REFERENCES audio_story(story_id)
        )
    """)

    # -------------------------------
    # LISTENING HISTORY TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listening_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            story_id INTEGER,
            listening_time REAL DEFAULT 0,
            skip_count INTEGER DEFAULT 0,
            replay_count INTEGER DEFAULT 0,
            completion_status INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(story_id) REFERENCES audio_story(story_id)
        )
    """)

    # -------------------------------
    # USAGE REPORT TABLE
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_report (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            play_count INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0,
            FOREIGN KEY(story_id) REFERENCES audio_story(story_id)
        )
    """)

    conn.commit()


def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    """
    General-purpose query executor.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    if commit:
        conn.commit()

    if fetch_one:
        return cursor.fetchone()

    if fetch_all:
        return cursor.fetchall()

    return None