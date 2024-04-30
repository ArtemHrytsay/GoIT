import configparser
from mongoengine import connect


config = configparser.ConfigParser()
config.read("config.ini")

usr    = config.get("DB", "USER")
pwd    = config.get("DB", "PASS")
db     = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")

connect(host=f"mongodb+srv://{usr}:{pwd}@{domain}/{db}?retryWrites=true&w=majority", ssl=True)
