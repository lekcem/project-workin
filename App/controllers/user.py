import os
from App.models import User, Report, ExcelData
from App.database import db
from flask import Blueprint, current_app
import pandas as pd

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


#test

def create_report(year,campus, excelfile): 
    newreport = Report(year=year, campus=campus, excelfile=excelfile)
    db.session.add(newreport)
    db.session.commit()
    return newreport

def get_all_reports():
    return Report.query.all()

def get_all_reports_json():
    reports = Report.query.all()
    if not reports:
        return []
    reports = [report.get_json() for report in reports]
    return reports

def ensure_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def process_excel_file(filepath, report_id):
    df = pd.read_excel(filepath, engine='openpyxl')


    for index, row in df.iterrows():
        department = row['department']  
        students = row['students']

        new_excel_data = ExcelData(
            department=department,
            students=students,
            report_id=report_id  
        )

        db.session.add(new_excel_data)

    db.session.commit()

    os.remove(filepath)  

def get_all_exceldatas():
    return ExcelData.query.all()   
 
def get_all_exceldatas_json():
    exceldatas = ExcelData.query.all()
    if not exceldatas:
        return []
    exceldatas = [exceldatas.get_json() for exceldatas in exceldatas]
    return exceldatas

def get_excel_data_for_report(report_id):
    excel_data = ExcelData.query.filter_by(report_id=report_id).all()
    return excel_data
