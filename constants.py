'''
Holds the global variables used by every script.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

# variable globals
CURRENT_USER = "Guest"    # indicates which type of user is logged in: Guest, Volunteer, Staff, Administrator
CURRENT_PAGE = -1    # indicates what page the application is currently on, this is the list index in window_manager.py


# hardcoded globals
ADMIN_PASSWORD = "ADMIN"    # holds the password given to Guests who sign up to become an Administrator
DELETE = False    # indicates if all data in the database should be deleted upon application start-up
