from pydantic_settings import BaseSettings
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR /'.env')
user = env('DATABASE_USER')
pw   = env('DATABASE_PASSWORD')
db   = env('DATABASE_NAME')
port = env('DATABASE_PORT')
host = env('DATABASE_HOST')


class Settings(BaseSettings):
    sqlalchemy_url       : str = f'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'
    secret_key           : str = env('SECRET_KEY')
    algorithm            : str = 'HS256'
    mail_username        : str = env('EMAIL_HOST_USER')
    mail_password        : str = env('EMAIL_HOST_PASSWORD')
    mail_from            : str = env('EMAIL_HOST_USER')
    mail_port            : int = env('EMAIL_PORT')
    mail_server          : str = host
    redis_host           : str = 'localhost'
    redis_port           : int = '6379'
    cloudinary_name      : str = 'name'
    cloudinary_api_key   : int = 123456789012345
    cloudinary_api_secret: str = 'secret'


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"


settings = Settings()
