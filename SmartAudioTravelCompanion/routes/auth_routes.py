from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


# -------------------------------
# REGISTER
# -------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'traveller')

        result = AuthService.register_user(username, password, role)

        if result["success"]:
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash(result["message"], "danger")

    return render_template('register.html')


# -------------------------------
# LOGIN
# -------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        result = AuthService.login_user(username, password)

        if result["success"]:
            user = result["user"]

            # Store session
            session['user_id'] = user["user_id"]
            session['username'] = user["username"]
            session['role'] = user["role"]

            # Redirect based on role
            if user["role"] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))

        else:
            flash(result["message"], "danger")

    return render_template('login.html')


# -------------------------------
# LOGOUT
# -------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('auth.login'))


# -------------------------------
# SESSION CHECK (UTILITY)
# -------------------------------
def login_required(role=None):
    def wrapper(func):
        from functools import wraps

        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))

            if role and session.get('role') != role:
                flash("Unauthorized access", "danger")
                return redirect(url_for('auth.login'))

            return func(*args, **kwargs)

        return decorated_function
    return wrapper