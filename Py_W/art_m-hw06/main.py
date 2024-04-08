import sqlite3
from random import randint, sample
from faker import Faker
from datetime import datetime


GROUPS = ['PyCore', 'PyWeb', 'DS']
DISCIPLINES = [
    "Python Core",
    "Python Web",
    "Data Science",
    "Career Skills",
    "English"
    ]

TEACHERS = 4
STUDENTS = 40
GRADES = 10


def init_db(db_path, path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # cur.execute("PRAGMA foreign_keys = ON;")

        with open(path, 'r') as file:
            sql = file.read()
        cur.executescript(sql)
        conn.commit()
        print("Process started successfully.")
    except sqlite3.Error as e:
        print(f"Error ocurred: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


def gen_data():
    fake = Faker()
    fake_groups = GROUPS
    fake_disciplines = DISCIPLINES

    fake_student_fn = [fake.first_name() for _ in range(STUDENTS)]
    fake_student_ln = [fake.unique.last_name() for _ in range(STUDENTS)]
    fake_teacher_fn = [fake.first_name() for _ in range(TEACHERS)]
    fake_teacher_ln = [fake.unique.last_name() for _ in range(TEACHERS)]

    today = datetime.now()
    start_date = datetime(2023, 9, 1)
    fake_dates = [fake.date_between(start_date, today) for _ in range(int(STUDENTS * GRADES))]

    return (fake_groups, fake_student_fn, fake_student_ln, fake_teacher_fn, fake_teacher_ln, fake_disciplines, fake_dates)


def data(_groups, _student_fn, _student_ln, _teacher_fn, _teacher_ln, _disciplines, _grades_dates):

    groups_list = [(group,) for group in _groups]
    students_list = [(first, last, randint(1, len(_groups))) for first, last in zip(_student_fn, _student_ln)]
    teachers_list = [(first, last) for first, last in zip(_teacher_fn, _teacher_ln)]
    disciplines = sample(_disciplines, len(_disciplines))
    discipline_list = list()

    for i, discipline in enumerate(disciplines):
        teacher_i = i % len(teachers_list)
        discipline_list.append((discipline, teacher_i + 1))

    grades_list = [(randint(1, len(students_list)), randint(1, len(discipline_list)), randint(1, 5), date) for date in _grades_dates]

    return groups_list, students_list, teachers_list, discipline_list, grades_list


def add_data(db_path, _groups, _students, _teachers, _disciplines, _grades):

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        add_groups =      ("INSERT INTO groups(group_name) VALUES (?)")
        add_students =    ("INSERT INTO students(first_name, last_name, group_id) VALUES (?, ?, ?)")
        add_teachers =    ("INSERT INTO teachers(first_name, last_name) VALUES (?, ?)")
        add_disciplines = ("INSERT INTO disciplines(discipline_name, teacher_id) VALUES (?, ?)")
        add_grades =      ("INSERT INTO grades(student_id, discipline_id, grade, grade_date) VALUES (?, ?, ?, ?)")

        cur.executemany(add_groups, _groups)
        cur.executemany(add_teachers, _teachers)
        cur.executemany(add_students, _students)
        cur.executemany(add_disciplines, _disciplines)
        cur.executemany(add_grades, _grades)

        conn.commit()
    except sqlite3.Error as e:
        print("Error adding data:", e)
        conn.rollback()
    finally:
        if conn:
            conn.close()

def main():
    db_path = 'hw6_database.db'
    path = 'sql/create_table.sql'

    init_db(db_path, path)
    groups, students, teachers, disciplines, grades = data(*(gen_data()))
    add_data(db_path, groups, students, teachers, disciplines, grades)
    print("DB has been successfully created")


if __name__ == '__main__':
    main()
