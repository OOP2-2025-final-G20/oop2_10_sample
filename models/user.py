from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    name = CharField()
    age = IntegerField()
    email = CharField(null=True)
    address = CharField(null=True)

    class Meta:
        database = db