from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey,Date
from config.db import session , engine


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id       = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

class Group(Base):
    __tablename__ = 'groups'
    id   = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id       = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group    = relationship('Group', backref='student')

class Discipline(Base):
    __tablename__ = 'disciplines'
    id         = Column(Integer, primary_key=True)
    name       = Column(String(175), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher    = relationship('Teacher', backref='disciplines')

class Grade(Base):
    __tablename__ = 'grades'
    id             = Column(Integer, primary_key=True)
    grade          = Column(Integer, nullable=False)
    grade_date     = Column('grade_date', Date, nullable=True)
    student_id     = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    disciplines_id = Column('discipline_id', ForeignKey('disciplines.id', ondelete='CASCADE'))
    student        = relationship('Student', backref='grade')
    discipline     = relationship('discipline', backref='grade')


Base.metadata.create_all(engine)
Base.metadata.bind = engine

session.commit()