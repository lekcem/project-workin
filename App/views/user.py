import os
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from werkzeug.utils import secure_filename
from.index import index_views

from App.controllers import (
    report_delete,
    get_report,
    get_excel_data,
    process_excel_file,
    get_all_exceldatas,
    get_all_exceldatas_json,
    get_excel_data_for_report,
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
@jwt_required()
def get_user_page():
    users = get_all_users()
    reports = get_all_reports()
    exceldatas = get_all_exceldatas()
    return render_template('users.html', users=users, reports=reports, exceldatas=exceldatas)

@user_views.route('/createuser', methods=['GET'])
@jwt_required()
def get_createuser_page():
    users = get_all_users()
    return render_template('createuser.html', users=users)

@user_views.route('/loginpage', methods=['GET'])
def get_loginpage_page():
    users = get_all_users()
    return render_template('login.html', users=users)


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
    year = request.form.get('year')
    campus = request.form.get('campus')

    ensure_upload_folder()

    if 'excelfile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['excelfile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)


        report = create_report(year, campus, filename)
        process_excel_file(filepath, report.id)  
        flash(f"Report for {year} created successfully!")
        return redirect(url_for('user_views.get_report_page'))

    else:
        flash('Invalid file format. Please upload an Excel file.')
        return redirect(request.url)


@user_views.route('/reports', methods=['GET'])
def get_report_page():
    reports = get_all_reports()
    exceldatas = get_all_exceldatas()
    return render_template('users.html', reports=reports, exceldatas=exceldatas)

@user_views.route('/api/reports', methods=['GET'])
def get_reports_action():
    reports = get_all_reports_json()
    return jsonify(reports)

@user_views.route('/reports', methods=['GET'])
def show_reports():
    reports = get_all_reports()
    return render_template('reports.html', reports=reports)



#ecxcetldat

@user_views.route('/api/exceldata', methods=['GET'])
def get_exceldata_for_report():
    report_id = request.args.get('report_id', type=int) 
    if report_id is None:
        return jsonify({"error": "Report ID is required"}), 400
    
    excel_data = get_excel_data_for_report(report_id)
    
    if not excel_data:
        return jsonify({"error": "No Excel data found for this report."}), 404
    
    result = []
    for data in excel_data:
        result.append({
            'id': data.id,
            'department': data.department,
            'students': data.students,
            'report_id': data.report_id
        })
    
    return jsonify(result)



#deletreport
@user_views.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = get_report(report_id)

    if report:
        report_delete(report_id)
        flash('Report deleted successfully!', 'success')
    else:
        flash('Report not found!', 'error')

    return redirect(url_for('user_views.show_reports'))


