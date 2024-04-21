import os

from dotenv import load_dotenv
from mongoengine import connect


load_dotenv()
user     = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PASSWORD")
domain   = os.environ.get("MONGODB_DOMAIN")

connect(
    host=f"mongodb+srv://{user}:{password}@{domain}/?retryWrites=true&w=majority",
    ssl=True
)
