from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings


URL = settings.sqlalchemy_url

engine    = create_engine(URL, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        db.close()
