from database.models.user import User
from database.models.traveller import Traveller
from database.models.admin import Admin


class AuthService:

    # -------------------------------
    # REGISTER USER
    # -------------------------------
    @staticmethod
    def register_user(username, password, role='traveller'):
        """
        Registers a new user and creates corresponding profile
        """

        # Check if user already exists
        existing_user = User.get_by_username(username)
        if existing_user:
            return {"success": False, "message": "Username already exists"}

        # Create user
        created = User.create_user(username, password, role)
        if not created:
            return {"success": False, "message": "User creation failed"}

        # Fetch created user
        user = User.get_by_username(username)

        # Create traveller or admin profile
        if role == 'traveller':
            Traveller.create_traveller(user.user_id)

        elif role == 'admin':
            Admin.create_admin(user.user_id)

        return {
            "success": True,
            "message": "User registered successfully",
            "user": user.to_dict()
        }

    # -------------------------------
    # LOGIN USER
    # -------------------------------
    @staticmethod
    def login_user(username, password):
        """
        Validates login and returns user data
        """

        user = User.validate_user(username, password)

        if not user:
            return {"success": False, "message": "Invalid username or password"}

        # Check role and attach additional info
        user_data = user.to_dict()

        if user.role == 'traveller':
            traveller = Traveller.get_by_user_id(user.user_id)
            user_data["profile"] = traveller.to_dict() if traveller else None

        elif user.role == 'admin':
            admin = Admin.get_by_user_id(user.user_id)
            user_data["profile"] = admin.to_dict() if admin else None

        return {
            "success": True,
            "message": "Login successful",
            "user": user_data
        }

    # -------------------------------
    # CHECK USER ROLE
    # -------------------------------
    @staticmethod
    def get_user_role(user_id):
        user = User.get_by_id(user_id)
        if user:
            return user.role
        return None

    # -------------------------------
    # VERIFY ADMIN ACCESS
    # -------------------------------
    @staticmethod
    def is_admin(user_id):
        return Admin.is_admin(user_id)

    # -------------------------------
    # CHANGE PASSWORD
    # -------------------------------
    @staticmethod
    def change_password(user_id, new_password):
        User.update_password(user_id, new_password)
        return {"success": True, "message": "Password updated successfully"}

    # -------------------------------
    # DELETE USER ACCOUNT
    # -------------------------------
    @staticmethod
    def delete_user(user_id):
        """
        Deletes user and associated profiles
        """

        role = AuthService.get_user_role(user_id)

        if role == 'traveller':
            Traveller.delete_traveller(user_id)

        elif role == 'admin':
            Admin.delete_admin(user_id)

        User.delete_user(user_id)

        return {"success": True, "message": "User deleted successfully"}