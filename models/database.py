'''
Handles the database.

Authors: Alex, Braden, Kaelan
Version: 02/01/2020

'''

from peewee import *

db = SqliteDatabase('nonprofit.db')


# User information
class User(Model):
    user_name = TextField()
    pass_word = TextField()
    account_age = DateTimeField()
    account_type = CharField()  # this could change to integer easily
    account_id = IntegerField()

    class Meta:
        database = db


# Event information
class Event(Model):
    event_date = DateTimeField()
    event_name = TextField()
    event_duration = IntegerField()
    event_description = TextField()
    attending_users = TextField()  # Currently, i want to store information in this field regarding who is attending the
    # event, based on the id, then use split to get a list of each attending member. There is probably a better way to
    # do it but we'll stick with this for now. (932 392 132 392 345 321 111 029 -> Braden, Kaelan, Alex, Tori, ...)

    class Meta:
        database = db


def connect():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Event])

