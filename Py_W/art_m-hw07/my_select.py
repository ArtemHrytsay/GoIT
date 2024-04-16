from sqlalchemy import func, desc

from config.models import Teacher, Group, Student, Discipline ,Grade
from config.db import session


def select_01():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.disciplines_id == 1).group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    return result

def select_03():
    result = session.query(Teacher.fullname, Discipline.name ) \
        .select_from(Teacher).join(Discipline).filter(Teacher.id == 5).all()
    return result

def select_06():
    result = session.query(Group.name, Student.fullname ) \
        .select_from(Group).join(Student).filter(Group.id == 2).all()
    return result

def select_07():
    result = session.query(Student.fullname, Group.name,Grade.grade,Discipline.name ) \
        .select_from(Student).join(Grade).join(Group).join(Discipline).filter(Grade.disciplines_id == 2,Group.id == 2).all()
    return result


def select_08():
    result = session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Teacher).join(Discipline).join(Grade).filter(Teacher.id == 4).group_by(Discipline.name,Teacher.fullname).order_by(desc('average_grade')).all()
    return result


def select_09():
    result = session.query(Student.fullname, Discipline.name) \
        .select_from(Discipline).join(Grade).join(Student).filter(Student.id == 2).group_by(Discipline.name,Student.fullname).all()
    return result


def select_10():
    result = session.query(Student.fullname, Discipline.name, Teacher.fullname ) \
        .select_from(Discipline).join(Grade).join(Student).join(Teacher).filter(Student.id == 2, Teacher.id == 4) \
            .group_by(Discipline.name,Student.fullname,Teacher.fullname ).all()
    return result


if __name__ == '__main__':
    print(select_01())
    #print(select_02())
    #print(select_03())
    #print(select_04())
    #print(select_05())
    #print(select_06())
    #print(select_07())
    #print(select_08())
    #print(select_09())
    # print(select_10())
