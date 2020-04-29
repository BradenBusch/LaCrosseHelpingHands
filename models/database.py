'''
Holds everything related to the database.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

from peewee import *


db = SqliteDatabase('nonprofit.sqlite')


# User information
class User(Model):
    user_id = AutoField()
    username = TextField()
    password = TextField()
    account_email = TextField()
    account_type = TextField()
    event_ids = TextField()  # String of each users events they are attending
    volunteer_hours = FloatField()
    total_donations = IntegerField()
    valid = BooleanField(default=True)

    class Meta:
        database = db


# Event information
class Event(Model):
    id = AutoField()
    day = CharField()
    month = CharField()
    year = CharField()
    start_date = CharField()  # the clock time the event starts at
    end_date = CharField()  # the clock time the event ends at
    name = CharField()
    location = CharField()
    description = TextField()
    volunteers_needed = IntegerField()
    volunteers_attending = IntegerField()
    volunteers_ids = TextField()  # String of each volunteers id that is attending this event
    donations = IntegerField()

    class Meta:
        database = db


# Holds information about the organization itself
class OrgEvent(Model):
    id = AutoField()
    name = CharField()
    donations = IntegerField()

    class Meta:
        database = db
