from datetime import datetime
from bson import json_util

from mongoengine import Document, CASCADE
from mongoengine.fields import  StringField,BooleanField

from config.db import mongoconect
mongoconect()

class User(Document):
    fullname     = StringField(max_length=100, required=True, unique=True)
    phone_number = StringField(max_length=30)
    is_send      = BooleanField(default=False)