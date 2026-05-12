from database.db import execute_query


class User:
    def __init__(self, user_id=None, username=None, password=None, role='traveller'):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    # -------------------------------
    # CREATE USER (REGISTER)
    # -------------------------------
    @staticmethod
    def create_user(username, password, role='traveller'):
        try:
            query = """
                INSERT INTO user (username, password, role)
                VALUES (?, ?, ?)
            """
            execute_query(query, (username, password, role), commit=True)
            return True
        except Exception as e:
            print("Error creating user:", e)
            return False

    # -------------------------------
    # GET USER BY USERNAME
    # -------------------------------
    @staticmethod
    def get_by_username(username):
        query = """
            SELECT * FROM user WHERE username = ?
        """
        row = execute_query(query, (username,), fetch_one=True)

        if row:
            return User(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            )
        return None

    # -------------------------------
    # GET USER BY ID
    # -------------------------------
    @staticmethod
    def get_by_id(user_id):
        query = """
            SELECT * FROM user WHERE user_id = ?
        """
        row = execute_query(query, (user_id,), fetch_one=True)

        if row:
            return User(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            )
        return None

    # -------------------------------
    # VALIDATE LOGIN
    # -------------------------------
    @staticmethod
    def validate_user(username, password):
        query = """
            SELECT * FROM user WHERE username = ? AND password = ?
        """
        row = execute_query(query, (username, password), fetch_one=True)

        if row:
            return User(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            )
        return None

    # -------------------------------
    # GET ALL USERS (ADMIN USE)
    # -------------------------------
    @staticmethod
    def get_all_users():
        query = "SELECT * FROM user"
        rows = execute_query(query, fetch_all=True)

        users = []
        for row in rows:
            users.append(User(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            ))
        return users

    # -------------------------------
    # DELETE USER (ADMIN USE)
    # -------------------------------
    @staticmethod
    def delete_user(user_id):
        query = "DELETE FROM user WHERE user_id = ?"
        execute_query(query, (user_id,), commit=True)

    # -------------------------------
    # UPDATE PASSWORD
    # -------------------------------
    @staticmethod
    def update_password(user_id, new_password):
        query = """
            UPDATE user SET password = ? WHERE user_id = ?
        """
        execute_query(query, (new_password, user_id), commit=True)

    # -------------------------------
    # CONVERT OBJECT TO DICTIONARY
    # -------------------------------
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role
        }