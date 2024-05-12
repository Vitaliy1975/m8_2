from mongoengine import  Document
from mongoengine.fields import StringField, BooleanField


class Contacts(Document):
    fullname = StringField()
    email = StringField()
    is_sent = BooleanField(default=False)