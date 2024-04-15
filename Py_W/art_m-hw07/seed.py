import datetime, calendar
import faker, random

import models

def seed(session):
    TEACHERS = 4
    STUDENTS = 40
    GRADES = 10

    GROUPS = ['PyCore', 'PyWeb', 'DS']
    DISCIPLINES = [
        "Python Core",
        "Python Web",
        "Data Science",
        "Career Skills",
        "English"
        ]
    
    _faker = faker.Faker()
    groups  (session, GROUPS)
    teachers(session, _faker, TEACHERS)
    disciplines(session, _faker, DISCIPLINES)
    students(session, _faker, STUDENTS)
    grades  (session, _faker, GRADES)


def groups(session, groups):
    count = 0
    result = ""
    for i, name in enumerate(groups):
        group = models.Group(name=name)
        session.add(group)
    else:
        try:
            session.commit()
            count = len(groups)
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"Error: {result}." if result else "."
    print(info)

def teachers(session, faker, number):
    count = 0
    result = ""
    data = list()

    for i in range(number):
        first_name  = faker.first_name()
        last_name   = faker.last_name()
        inf = (i, first_name, last_name)
        data.append(inf)
        teacher = models.Teacher(first_name=first_name, last_name=last_name)
        session.add(teacher)
    else:
        try:
            session.commit()
            count = number
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"Error: {result}." if result else "."
    print(info)

def disciplines(session, faker, disciplines):
    count = 0
    result = ""
    teachers = session.query(models.Teacher).all()
    data = list()
    for i, name in enumerate(disciplines):
        teacher_id = random.choice(teachers).id
        inf = (i, name, teacher_id)
        data.append(inf)
        teacher = models.Discipline(name=name, teacher_id=teacher_id)
        session.add(teacher)
    else:
        try:
            session.commit()
            count = len(disciplines)
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"Error: {result}." if result else "."
    print(info)
    
def students(session, faker, number):
    count = 0
    result = ""
    groups = session.query(models.Group).all()
    data = list()
    for i in range(number):
        group_id    = random.choice(groups).id
        first_name  = faker.first_name()
        last_name   = faker.last_name()
        inf = (i, first_name, last_name, group_id)
        data.append(inf)
        student = models.Student(first_name=first_name, last_name=last_name, group_id=group_id)
        result = session.add(student)
    else:
        try:
            session.commit()
            count = number
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"Error: {result}." if result else "."
    print(info)
    return data

def grades(session, faker, max_grades):
    count = 0
    result = ""
    disciplines = session.query(models.Discipline).all()
    students = session.query(models.Student).all()
    data = list()
    _calendar = calendar.Calendar(calendar.MONDAY)
    i = 0
    for _ in range(0, max_grades):
        for student in students:
            year    = 2023
            month   = random.randint(1,12)
            days    = []
            for date in _calendar.itermonthdates(year, month):
                if date.month == month and date.weekday() < 5:
                    days.append(date.day)
            timestamp = datetime.datetime(
                            year,
                            month,
                            random.choice(days),
                            random.randint(9, 21),
                            random.randint(1, 59),
                            random.randint(1, 59)
                        )
            discipline_id   = random.choice(disciplines).id
            student_id  = student.id
            timestamp    = timestamp.isoformat()
            grade       = random.randint(1, 12)
            inf = (i, discipline_id, student_id, timestamp, grade)
            data.append(inf)
            grade = models.Grade(discipline_id=discipline_id, student_id=student_id, datetime=timestamp, grade=grade)
            session.add(grade)
            i += 1
    else:
        try:
            session.commit()
            count = max_grades
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"Error: {result}." if result else "."
    print(info)
