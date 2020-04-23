'''
Holds the global variables used by every script.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/05/2020

'''

# variable globals
CURRENT_USER = "Guest"    # indicates which type of user is logged in: Guest, Volunteer, Staff, Administrator
CURRENT_PAGE = -1    # indicates what page the application is currently on, this is the list index in window_manager.py
PREV_PAGE = -1    # indicates what page the user came from to arrive on the current page
CURRENT_DATE = -1    # indicates what date was clicked on the calendar by the user
CURRENT_USER_ID = -1   # indicates the user_id of the logged in user for database purposes

# hardcoded globals
STAFF_CODE = "STAFF"    # holds the code given to Guests who sign up to become a Staff member
ADMIN_CODE = "ADMIN"    # holds the code given to Guests who sign up to become an Administrator
ORG_ID = 1    # holds the organization's "event ID" so that donations can be made to it

# page identification
PAGE_LOGIN_SIGNUP = 0
PAGE_LOGIN = 1
PAGE_NEW_ACCOUNT = 2
PAGE_HOME = 3
PAGE_CAL = 4
PAGE_ACCOUNT = 5
PAGE_PRIVILEGES = 6
PAGE_ABOUT = 7
PAGE_CONTACT = 8
PAGE_HELP = 9
PAGE_SEARCH = 10
