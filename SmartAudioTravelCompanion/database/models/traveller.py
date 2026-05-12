from database.db import execute_query


class Traveller:
    def __init__(self, traveller_id=None, user_id=None, interest_profile=None, privacy_setting='accepted'):
        self.traveller_id = traveller_id
        self.user_id = user_id
        self.interest_profile = interest_profile  # stored as string (JSON-like)
        self.privacy_setting = privacy_setting

    # -------------------------------
    # CREATE TRAVELLER PROFILE
    # -------------------------------
    @staticmethod
    def create_traveller(user_id):
        default_profile = "history:0,nature:0,culture:0,legends:0"

        query = """
            INSERT INTO traveller (user_id, interest_profile, privacy_setting)
            VALUES (?, ?, ?)
        """
        execute_query(query, (user_id, default_profile, 'accepted'), commit=True)

    # -------------------------------
    # GET TRAVELLER BY USER ID
    # -------------------------------
    @staticmethod
    def get_by_user_id(user_id):
        query = """
            SELECT * FROM traveller WHERE user_id = ?
        """
        row = execute_query(query, (user_id,), fetch_one=True)

        if row:
            return Traveller(
                traveller_id=row["traveller_id"],
                user_id=row["user_id"],
                interest_profile=row["interest_profile"],
                privacy_setting=row["privacy_setting"]
            )
        return None

    # -------------------------------
    # UPDATE INTEREST PROFILE
    # -------------------------------
    @staticmethod
    def update_interest_profile(user_id, new_profile):
        query = """
            UPDATE traveller
            SET interest_profile = ?
            WHERE user_id = ?
        """
        execute_query(query, (new_profile, user_id), commit=True)

    # -------------------------------
    # UPDATE PRIVACY SETTING
    # -------------------------------
    @staticmethod
    def update_privacy_setting(user_id, setting):
        query = """
            UPDATE traveller
            SET privacy_setting = ?
            WHERE user_id = ?
        """
        execute_query(query, (setting, user_id), commit=True)

    # -------------------------------
    # RESET INTEREST PROFILE
    # -------------------------------
    @staticmethod
    def reset_interest_profile(user_id):
        default_profile = "history:0,nature:0,culture:0,legends:0"

        query = """
            UPDATE traveller
            SET interest_profile = ?
            WHERE user_id = ?
        """
        execute_query(query, (default_profile, user_id), commit=True)

    # -------------------------------
    # DELETE TRAVELLER PROFILE
    # -------------------------------
    @staticmethod
    def delete_traveller(user_id):
        query = """
            DELETE FROM traveller WHERE user_id = ?
        """
        execute_query(query, (user_id,), commit=True)

    # -------------------------------
    # CONVERT PROFILE STRING → DICTIONARY
    # -------------------------------
    def get_interest_dict(self):
        profile_dict = {}

        if self.interest_profile:
            items = self.interest_profile.split(',')
            for item in items:
                key, value = item.split(':')
                profile_dict[key] = float(value)

        return profile_dict

    # -------------------------------
    # CONVERT DICTIONARY → PROFILE STRING
    # -------------------------------
    @staticmethod
    def dict_to_profile_string(profile_dict):
        return ",".join([f"{k}:{v}" for k, v in profile_dict.items()])

    # -------------------------------
    # CONVERT OBJECT TO DICT
    # -------------------------------
    def to_dict(self):
        return {
            "traveller_id": self.traveller_id,
            "user_id": self.user_id,
            "interest_profile": self.interest_profile,
            "privacy_setting": self.privacy_setting
        }