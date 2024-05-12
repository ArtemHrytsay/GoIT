from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from connect import engine

Base = declarative_base()


class Author(Base):
    __tablename__ = 'app_quotes_author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(250), nullable=False)
    born_date = Column(String(20))
    born_location = Column(String(250))
    description = Column(Text)
    user_id = Column(Integer)


class Quote(Base):
    __tablename__ = 'app_quotes_quote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tags = Column(ARRAY(Text))
    author_id = Column(Integer, ForeignKey('app_quotes_author.id', ondelete='CASCADE'), default=1)
    quote = Column(Text)
    quote_rel = relationship('Author', backref='app_quotes_quote')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
