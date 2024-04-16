from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from config.db import session , engine
from config.models import Teacher, Group, Student, Discipline ,Grade
from faker import Faker
from random import randint


STUDENTS    = 40
TEACHERS    = 5
GROUPS      = 3
DISCIPLINES = 8
GRADES      = 10

Base = declarative_base()

fake = Faker((['uk-UA']))

Base.metadata.create_all(engine)
Base.metadata.bind = engine

for _ in range(TEACHERS):
    new_teachers = Teacher(fullname=fake.name())
    session.add(new_teachers)

for _ in range(GROUPS):
    new_groups = Group(name=fake.safe_color_name())
    session.add(new_groups)

for _ in range(STUDENTS):
    new_student = Student(fullname=fake.name(), group_id=randint(1, GROUPS ) )
    session.add(new_student)

for _ in range(DISCIPLINES):
    new_disciplines = Discipline(name=fake.job(), teacher_id=randint(1, TEACHERS) )
    session.add(new_disciplines)

for num_st in range(1, STUDENTS + 1):
    for _ in range(GRADES):
        new_grade = Grade(grade=randint(4, 12), grade_date=fake.date_this_decade(),student_id=num_st, disciplines_id=randint(1, DISCIPLINES))
        session.add(new_grade)

session.commit()
