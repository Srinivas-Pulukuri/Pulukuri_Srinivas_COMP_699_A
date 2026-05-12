from database.db import execute_query


class Admin:
    def __init__(self, admin_id=None, user_id=None, role='admin'):
        self.admin_id = admin_id
        self.user_id = user_id
        self.role = role

    # -------------------------------
    # CREATE ADMIN (PROMOTE USER)
    # -------------------------------
    @staticmethod
    def create_admin(user_id, role='admin'):
        query = """
            INSERT INTO admin (user_id, role)
            VALUES (?, ?)
        """
        execute_query(query, (user_id, role), commit=True)

    # -------------------------------
    # GET ADMIN BY USER ID
    # -------------------------------
    @staticmethod
    def get_by_user_id(user_id):
        query = """
            SELECT * FROM admin WHERE user_id = ?
        """
        row = execute_query(query, (user_id,), fetch_one=True)

        if row:
            return Admin(
                admin_id=row["admin_id"],
                user_id=row["user_id"],
                role=row["role"]
            )
        return None

    # -------------------------------
    # CHECK IF USER IS ADMIN
    # -------------------------------
    @staticmethod
    def is_admin(user_id):
        query = """
            SELECT * FROM admin WHERE user_id = ?
        """
        row = execute_query(query, (user_id,), fetch_one=True)
        return row is not None

    # -------------------------------
    # GET ALL ADMINS
    # -------------------------------
    @staticmethod
    def get_all_admins():
        query = "SELECT * FROM admin"
        rows = execute_query(query, fetch_all=True)

        admins = []
        for row in rows:
            admins.append(Admin(
                admin_id=row["admin_id"],
                user_id=row["user_id"],
                role=row["role"]
            ))
        return admins

    # -------------------------------
    # REMOVE ADMIN (DEMOTE)
    # -------------------------------
    @staticmethod
    def delete_admin(user_id):
        query = """
            DELETE FROM admin WHERE user_id = ?
        """
        execute_query(query, (user_id,), commit=True)

    # -------------------------------
    # UPDATE ADMIN ROLE
    # -------------------------------
    @staticmethod
    def update_role(user_id, new_role):
        query = """
            UPDATE admin
            SET role = ?
            WHERE user_id = ?
        """
        execute_query(query, (new_role, user_id), commit=True)

    # -------------------------------
    # CONVERT OBJECT TO DICTIONARY
    # -------------------------------
    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "user_id": self.user_id,
            "role": self.role
        }