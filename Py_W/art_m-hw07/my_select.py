import sqlalchemy.sql.functions as func

from sqlalchemy import func, desc, and_, true
from main import Connection

from models import Group, Student, Teacher, Discipline, Grade


def select_01(criterion = None, limit = 5):
    "First five studens with highest average grade."
    result = Connection.session().query(
        Student.first_name,
        Student.last_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'),
        func.count('*').label("count")
    ).select_from(Grade).join(Student)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .group_by(Student.id)\
        .order_by(desc('average_grade'))\
        .limit(limit)
    return result

def select_02(criterion = Discipline.id == 1, limit = 1):
    "First student with highest average grade by discipline."
    result = Connection.session().query(
        Discipline.name,
        Student.first_name,
        Student.last_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'),
        func.count('*').label("count"),
    ).select_from(Grade).join(Student).join(Discipline)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .group_by(Discipline.name, Student.id)\
        .order_by(desc('average_grade'))\
        .limit(limit)
    return result

def select_03(criterion = Discipline.id == 1, limit = None):
    "Average grade in groups by discipline."
    result = Connection.session().query(
        Group.name,
        Discipline.id,
        Discipline.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'),
        func.count('*').label("count")
    ).select_from(Grade).join(Student).join(Group).join(Discipline)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .group_by(Group.id, Group.name, Discipline.id, Discipline.name)\
        .order_by(Group.id, Discipline.id)\
        .limit(limit)
    return result

def select_04(criterion = None, limit = None):
    "Average grade."
    result = Connection.session().query(
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade)\
    .limit(limit)
    return result

def select_05(criterion = None, limit = None):
    "Disciplines taught by the teacher."
    result = Connection.session().query(
        Teacher.first_name,
        Teacher.last_name,
        Discipline.name
    ).select_from(Teacher).join(Discipline)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result

def select_06(criterion = Group.id == 1, limit = None):
    "Students in the group."
    result = Connection.session().query(
        Group.name,
        Student.first_name,
        Student.last_name
    ).select_from(Group).join(Student)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result

def select_07(criterion = and_(Discipline.id == 1, Group.id == 1), limit = None):
    "Grades of group by discipline."
    result = Connection.session().query(
        Group.name,
        Discipline.name,
        Student.first_name,
        Student.last_name,
        Grade.grade,
        Grade.datetime
    ).select_from(Grade).join(Discipline).join(Student).join(Group)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result

def select_08(criterion = Teacher.id == 1, limit = None):
    "Average grade given by teacher for his disciplines."
    result = Connection.session().query(
        Discipline.name,
        Teacher.first_name,
        Teacher.last_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'),
        func.count('*').label("count")
    ).select_from(Grade).join(Discipline).join(Teacher)\
        .group_by(Teacher.id, Discipline.id)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result

def select_09(criterion = Student.id == 1, limit = None):
    "Disciplines by the student."
    result = Connection.session().query(
        Student.first_name,
        Student.last_name,
        Discipline.name,
    ).select_from(Grade).join(Discipline).join(Student)\
        .group_by(Student.id, Discipline.id)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result

def select_10(criterion = and_(Teacher.id == 1, Student.id == 1), limit = None):
    "Disciplines teacher teachs to student."
    result = Connection.session().query(
        Teacher.first_name,
        Teacher.last_name,
        Discipline.name,
        Student.first_name,
        Student.last_name
    ).select_from(Grade).join(Discipline).join(Teacher).join(Student)\
        .group_by(Teacher.id, Discipline.id, Student.id)\
        .filter(criterion if id(criterion) != id(False) else true())\
        .limit(limit)
    return result
