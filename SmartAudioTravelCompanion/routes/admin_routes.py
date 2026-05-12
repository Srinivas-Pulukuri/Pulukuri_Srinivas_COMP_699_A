from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from routes.auth_routes import login_required

from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)


# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
@admin_bp.route('/admin/dashboard')
@login_required(role='admin')
def dashboard():
    stories = AdminService.get_all_stories()
    reports = AdminService.get_all_reports()

    return render_template('admin.html', stories=stories, reports=reports)


# -------------------------------
# UPLOAD STORY
# -------------------------------
@admin_bp.route('/admin/upload', methods=['POST'])
@login_required(role='admin')
def upload_story():
    title = request.form.get('title')
    category = request.form.get('category')
    duration = request.form.get('duration')
    file = request.files.get('file')

    try:
        duration = float(duration)
    except:
        duration = 0

    result = AdminService.upload_story(title, category, duration, file)

    if result["success"]:
        flash("Story uploaded successfully", "success")
    else:
        flash(result["message"], "danger")

    return redirect(url_for('admin.dashboard'))


# -------------------------------
# UPDATE STORY
# -------------------------------
@admin_bp.route('/admin/update/<int:story_id>', methods=['POST'])
@login_required(role='admin')
def update_story(story_id):
    title = request.form.get('title')
    category = request.form.get('category')
    duration = request.form.get('duration')

    try:
        duration = float(duration)
    except:
        duration = 0

    AdminService.update_story(story_id, title, category, duration)

    flash("Story updated successfully", "success")
    return redirect(url_for('admin.dashboard'))


# -------------------------------
# DELETE STORY
# -------------------------------
@admin_bp.route('/admin/delete/<int:story_id>', methods=['POST'])
@login_required(role='admin')
def delete_story(story_id):
    AdminService.delete_story(story_id)

    flash("Story deleted successfully", "warning")
    return redirect(url_for('admin.dashboard'))


# -------------------------------
# UPDATE AUDIO FILE
# -------------------------------
@admin_bp.route('/admin/update_file/<int:story_id>', methods=['POST'])
@login_required(role='admin')
def update_file(story_id):
    file = request.files.get('file')

    result = AdminService.update_story_file(story_id, file)

    if result["success"]:
        flash("Audio file updated", "success")
    else:
        flash(result["message"], "danger")

    return redirect(url_for('admin.dashboard'))


# -------------------------------
# VIEW REPORT FOR STORY
# -------------------------------
@admin_bp.route('/admin/report/<int:story_id>')
@login_required(role='admin')
def view_report(story_id):
    report = AdminService.get_story_report(story_id)

    return render_template('admin.html', selected_report=report)


# -------------------------------
# RESET REPORT
# -------------------------------
@admin_bp.route('/admin/reset_report/<int:story_id>', methods=['POST'])
@login_required(role='admin')
def reset_report(story_id):
    AdminService.reset_report(story_id)

    flash("Report reset successfully", "info")
    return redirect(url_for('admin.dashboard'))


# -------------------------------
# SYSTEM HEALTH CHECK
# -------------------------------
@admin_bp.route('/admin/health')
@login_required(role='admin')
def system_health():
    status = AdminService.system_health()

    return render_template('admin.html', system_status=status)