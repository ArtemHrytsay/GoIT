from config.models import User
from mongoengine.errors import NotUniqueError
from config.db import mongoconect
from faker import Faker


fake = Faker()

def seed(count=0):
    mongoconect()
    if count == 0:
        return None
    for el in range(count):
        try:
            user = User(fullname=fake.name(), phone_number=fake.phone_number())
            user.save()
        except Exception as e:
            print(e)
        except AttributeError:
            print("a") 
        
seed(100)
