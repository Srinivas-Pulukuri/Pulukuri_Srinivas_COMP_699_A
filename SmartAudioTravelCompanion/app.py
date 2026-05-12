from flask import Flask, redirect, url_for, session

from config import Config
from database.db import init_db

# Import all blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.audio_routes import audio_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)

    # -------------------------------
    # CONFIGURATION
    # -------------------------------
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    # -------------------------------
    # DATABASE INIT
    # -------------------------------
    init_db()

    # -------------------------------
    # REGISTER BLUEPRINTS
    # -------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(admin_bp)

    # -------------------------------
    # DEFAULT ROUTE (FIXED)
    # -------------------------------
    @app.route('/')
    def home():
        # If user already logged in
        if 'user_id' in session:
            if session.get('role') == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))

        # If not logged in → go to login page
        return redirect(url_for('auth.login'))

    return app


# -------------------------------
# RUN APPLICATION
# -------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)