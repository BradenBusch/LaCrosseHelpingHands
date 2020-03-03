'''
Holds the global variables used by every script.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

# variable globals
CURRENT_USER = "Guest"    # indicates which type of user is logged in: Guest, Volunteer, Staff, Administrator
CURRENT_PAGE = -1    # indicates what page the application is currently on, this is the list index in window_manager.py
PREV_PAGE = -1    # indicates what page the user came from to arrive on the current page
CURRENT_DATE = -1    # indicates what date was clicked on the calendar by the user

# hardcoded globals
ADMIN_PASSWORD = "ADMIN"    # holds the password given to Guests who sign up to become an Administrator
DELETE = False    # indicates if all data in the database should be deleted upon application start-up

# page identification
PAGE_LOGIN_SIGNUP = 0
PAGE_LOGIN = 1
PAGE_NEW_ACCOUNT = 2
PAGE_HOME = 3
PAGE_CAL = 4
PAGE_ABOUT = 5
PAGE_CONTACT = 6
PAGE_SEARCH = 7
PAGE_ACCOUNT = 8
