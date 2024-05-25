import configparser, pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

file_config = pathlib.Path(__file__).parent.parent.joinpath('database/config.ini')
config      = configparser.ConfigParser()
config.read(file_config)

user     = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
db_name  = config.get('DB', 'DB_NAME')
domain   = config.get('DB', 'DOMAIN')
port     = config.get('DB', 'PORT')
url      = f'postgresql://{user}:{password}@{domain}:{port}/{db_name}'

engine   = create_engine(url, echo=True)

DBSession = sessionmaker(bind=engine)
session   = DBSession()

# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
