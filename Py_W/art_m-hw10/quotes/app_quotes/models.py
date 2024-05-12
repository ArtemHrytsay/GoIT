from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    id            = models.AutoField(primary_key=True)
    fullname      = models.CharField(unique=True, max_length=100)
    born_date     = models.DateField(null=False)
    born_location = models.CharField(max_length=500, null=False)
    description   = models.TextField(null=False)
    user          = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    id     = models.AutoField(primary_key=True)
    quote  = models.TextField(unique=True, null=False)
    author = models.ForeignKey(Author, to_field="id", on_delete=models.CASCADE)
    tags   = ArrayField(models.CharField(max_length=50), null=False, blank=True)

    def __str__(self):
        return f"{self.tags}"
