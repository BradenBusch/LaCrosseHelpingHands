'''
Handles the database.

Authors: Alex, Braden, Kaelan
Version: 02/01/2020

'''

from peewee import *

db = SqliteDatabase('nonprofit.sqlite')


# User information
# TODO might just be able to change account id to an iterating number starting at 1 instead of random nums
class User(Model):
    account_id = IntegerField(unique=True)
    username = TextField()
    password = TextField()
    account_email = TextField()
    account_type = TextField()

    class Meta:
        database = db


# Event information
class Event(Model):
    event_id = IntegerField(unique=True)
    event_date = DateTimeField()
    event_name = CharField()
    event_duration = IntegerField()
    event_description = TextField()
    attending_users = TextField()
    # TODO nvm we do this with joins, i got it. many event for many users (users can go to more than one event)
    # Currently, i want to store information in this field regarding who is attending the
    # event, based on the id, then use split to get a list of each attending member. There is probably a better way to
    # do it but we'll stick with this for now. (932 392 132 392 345 321 111 029 -> Braden, Kaelan, Alex, Tori, ...)

    class Meta:
        database = db


class EventAttendance(Model):
    event_id = ForeignKeyField(User)
    account_id = ForeignKeyField(Event)
    event_id = IntegerField()
    account_id = IntegerField()

    class Meta:
        database = db
