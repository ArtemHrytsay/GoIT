import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = configparser.ConfigParser()
config.read("config.ini")

user     = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
db_name  = config.get('DB', 'DB_NAME')
domain   = config.get('DB', 'DOMAIN')
port     = config.get('DB', 'PORT')
url      = f'postgresql://{user}:{password}@{domain}:{port}/{db_name}'

engine   = create_engine(url, echo=True)

DBSession = sessionmaker(bind=engine)
session   = DBSession()
