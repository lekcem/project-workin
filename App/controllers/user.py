from App.models import User, Report
from App.database import db

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
"""
  with open('todos.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      new_todo = Todo(text=row['text'])  #create object
      #update fields based on records
      new_todo.done = True if row['done'] == 'true' else False
      new_todo.user_id = int(row['user_id'])
      db.session.add(new_todo)  #queue changes for saving
    db.session.commit()
    """
def create_report(year,campus, excelfile): 
    newreport = Report(year=year, campus=campus, excelfile=excelfile)
    db.session.add(newreport)
    db.session.commit()
    return newreport

def get_report(id):
    return Report.query.get(id)

def get_report_by_year(year):
    return Report.query.filter_by(year=year).first()

def get_report_by_campus(campus):
    return Report.query.filter_by(campus=campus).first()

def update_report(id, year, campus, excelfile):
    report = get_report(id)
    if report:
        report.year = year
        report.campus = campus
        report.excelfile = excelfile
        db.session.add(report)
        return db.session.commit()
    return None

def get_all_reports():
    return Report.query.all()

def get_all_reports_json():
    reports = Report.query.all()
    if not reports:
        return []
    reports = [report.get_json() for report in reports]
    return reports
