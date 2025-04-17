import os
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from werkzeug.utils import secure_filename
from.index import index_views

from App.controllers import (
    ensure_upload_folder,
    create_user,
    allowed_file,
    create_report,
    get_all_reports,
    get_all_reports_json,
   
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')




#test
@user_views.route('/reports', methods=['POST'])
def create_report_action():
    # Get form data
    year = request.form.get('year')
    campus = request.form.get('campus')

    ensure_upload_folder()

    # Handle file upload
    if 'excelfile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['excelfile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Secure the filename and save it
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Now create the report
        report = create_report(year, campus, filepath)
        flash(f"Report for {year} created successfully!")
        return redirect(url_for('user_views.get_report_page'))

    else:
        flash('Invalid file format. Please upload an Excel file.')
        return redirect(request.url)


@user_views.route('/reports', methods=['GET'])
def get_report_page():
    reports = get_all_reports()
    return render_template('users.html', reports=reports)

@user_views.route('/api/reports', methods=['GET'])
def get_reports_action():
    reports = get_all_reports_json()
    return jsonify(reports)

@user_views.route('/api/reports', methods=['POST'])
def create_report_endpoint():
    data = request.json
    report = create_report(data['year'], data['campus'], data['excelfile'])
    return jsonify({'message': f"report {report.year} created with id {report.id}"})
