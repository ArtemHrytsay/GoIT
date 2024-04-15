import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as extension
from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, text

import registrator

Base = extension.declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id          = Column("id"         , Integer     , primary_key = True)
    name        = Column("name"       , String(128) , nullable=False    , unique=True)

    __table_args__ = (UniqueConstraint("name", name = "uc_groups")  ,)

    students    = orm.relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id          = Column("id"         , Integer     , primary_key = True)
    group_id    = Column("group_id"   , Integer     , ForeignKey('groups.id'    , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    first_name  = Column("first_name" , String(128) , nullable=False)
    last_name   = Column("last_name"  , String(128) , nullable=False)
    middle_name = Column("middle_name", String(128) , nullable=True)

    __table_args__ = (UniqueConstraint("first_name", "last_name", name = "uc_students") ,)

    group           = orm.relationship("Group"  , back_populates="students")
    student_grades  = orm.relationship("Grade"  , back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    id          = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    first_name  = Column("first_name" , String(128) , nullable=False)
    last_name   = Column("last_name"  , String(128) , nullable=False)
    middle_name = Column("middle_name", String(128) , nullable=True)

    __table_args__ = (UniqueConstraint("first_name", "last_name", name = "uc_teachers") ,)

    disciplines     = orm.relationship("Discipline", back_populates="teacher", uselist=False)


class Discipline(Base):
    __tablename__ = "disciplines"
    id          = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    teacher_id  = Column("teacher_id" , Integer     , ForeignKey('teachers.id'  , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    name        = Column("name"       , String(128) , nullable=False    , unique=True)

    __table_args__ = (UniqueConstraint("name", name = "uc_disciplines") ,)

    teacher           = orm.relationship("Teacher"    , back_populates="disciplines")
    discipline_grades = orm.relationship("Grade"      , back_populates="discipline")


class Grade(Base):
    __tablename__ = "grades"
    id            = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    discipline_id = Column("discipline_id"  , Integer     , ForeignKey('disciplines.id'   , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    student_id    = Column("student_id" , Integer     , ForeignKey('students.id'  , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    datetime      = Column("datetime"   , DateTime    , nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    grade         = Column("grade"      , Integer     , nullable=False)

    __table_args__ = (UniqueConstraint("discipline_id", "student_id", "datetime", name = "uc_grades")   ,)

    discipline  = orm.relationship("Discipline"    , back_populates="discipline_grades")
    student     = orm.relationship("Student"   , back_populates="student_grades")

metadata = MetaData()

# class MODELS(registrator):    ...
# MODELS.register("", __name__, globals(), Base,["__builtins__", "Base"])
# registry = MODELS()
