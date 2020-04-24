'''
Administrator Privileges page, where Administrators can view all users and events for
the organization, as well as generate reports.

Accessibile by: Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/23/2020

'''
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial

try:
    from non_profit.models.database import *
    from non_profit import constants as cs
except:
    from models.database import *
    import constants as cs


# TODO fix the following:
#  -> Complete all marked areas
class Privileges(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'privileges')
        self.setWindowTitle('Administrator Privileges')
        self.win = None
        self.this_page = cs.PAGE_PRIVILEGES
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        self.vbox_screen = QVBoxLayout()
        
        self.hbox_1 = QHBoxLayout()
        self.spacer_1 = QLabel("")
        self.spacer_1.setProperty('class', 'priv-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)
        
        # create the top bar of tabs for the application
        self.top_bar()
        
        # create HBoxes
        self.hbox_2 = QHBoxLayout()
        self.hbox_screen = QHBoxLayout()
        
        self.account_label = QLabel("Administrator Privileges")
        self.account_label.setProperty('class', 'cal-label')
        self.account_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.account_label)
        
        # Divide the screen into halves
        self.vbox_1 = QVBoxLayout()
        self.vbox_2 = QVBoxLayout()
        
        # create title HBoxes
        self.hbox_users = QHBoxLayout()
        self.hbox_events = QHBoxLayout()
        
        # create label for the users
        self.events_label = QLabel("All Users")
        self.events_label.setProperty('class', 'home-events-label')
        self.events_label.setFixedHeight(40)
        self.events_label.setAlignment(Qt.AlignCenter)
        self.hbox_users.addWidget(self.events_label)
        
        # create the generate reports button
        self.gen_rep_users_btn = QPushButton('Generate Report')
        self.gen_rep_users_btn.setProperty('class', 'long-bar-btn')
        self.gen_rep_users_btn.clicked.connect(self.generate_all_users_report)
        self.gen_rep_users_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.hbox_users.addWidget(self.gen_rep_users_btn)
        self.vbox_1.addLayout(self.hbox_users)
        
        # create label for the events
        self.events_label = QLabel("All Events")
        self.events_label.setProperty('class', 'home-events-label')
        self.events_label.setFixedHeight(40)
        self.events_label.setAlignment(Qt.AlignCenter)
        self.hbox_events.addWidget(self.events_label)
        
        # create the generate reports button
        self.gen_rep_events_btn = QPushButton('Generate Report')
        self.gen_rep_events_btn.setProperty('class', 'long-bar-btn')
        self.gen_rep_events_btn.clicked.connect(self.generate_all_events_report)
        self.gen_rep_events_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.hbox_events.addWidget(self.gen_rep_events_btn)
        self.vbox_2.addLayout(self.hbox_events)
        
        # populate both scroll areas
        self.populate_all_users()
        self.populate_all_events()
        
        # add two VBoxes to top level HBox
        self.hbox_screen.addLayout(self.vbox_1)
        self.hbox_screen.addLayout(self.vbox_2)
        
        # add HBoxes to top level VBox
        self.vbox_screen.addLayout(self.hbox_2)
        self.vbox_screen.addLayout(self.hbox_screen)
        
        # create spacer for bottom of screen
        self.hbox_3 = QHBoxLayout()
        self.spacer_2 = QLabel("")
        self.spacer_2.setProperty('class', 'priv-bottom-spacer-label')
        self.hbox_3.addWidget(self.spacer_2)
        self.vbox_screen.addLayout(self.hbox_3)
        
        # set up the layout
        self.setLayout(self.vbox_screen)
        
        # set the geometry of the window
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = 0
        self.y_coord = 40
        self.width = sys_width
        self.height = sys_height
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # populate all users with information about each user
    def populate_all_users(self):
        # Build the scroll areas
        self.all_users_widget = QWidget()
        self.all_users_vbox = QVBoxLayout()
        self.all_users_widget.setLayout(self.all_users_vbox)
        self.all_users = QScrollArea()
        self.all_users.setWidget(self.all_users_widget)
        self.all_users.setWidgetResizable(True)
        self.all_users.setFixedHeight(575)
        sys_width, sys_height = self.screen_resolution()
        self.all_users.setFixedWidth((sys_width // 2) - 35)
        self.all_users.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # TODO fill user scroll area with proper information
        has_users = False
        try:
            users = User.select()
            has_users = True
        except:
            has_users = False
        
        # there are no users of the system (this should never be true because an admin has to be looking at it)
        if not has_users:
            hbox = QHBoxLayout()
            no_users = QLabel('There are no other registered users in the organization.')
            no_users.setAlignment(Qt.AlignCenter)
            no_users.setProperty('class', 'no-events-label')
            hbox.addWidget(no_users)
            self.all_users_vbox.addLayout(hbox)
            self.vbox_1.addWidget(self.all_users)
            return
        
        # holds user ids from database
        # user_ids = ids.split(' ')
        
        # master list to hold all users
        master_users = []
        
        # build up all event data
        for user in users:
            # retrieve all relevant information # TODO replace these event attributes with the user attributes instead
            master_users.append([user.username,
                                 user.account_email,
                                 user.total_donations,
                                 user.volunteer_hours,
                                 user.user_id])
        
        # sort the users alphabetically by username
        # master_users.sort(key=lambda x: (int(x[4]), int(x[2]), int(x[3]), x[5]))
        master_users.sort(key=lambda x: x[0])

        # if there are no events the user has signed up for
        if len(master_users) == 0:
            # inform the user that no events have been scheduled yet
            hbox = QHBoxLayout()
            no_users = QLabel('There are no other registered users in the organization.')
            no_users.setAlignment(Qt.AlignCenter)
            no_users.setProperty('class', 'no-events-label')
            hbox.addWidget(no_users)
            self.all_users_vbox.addLayout(hbox)
            self.vbox_1.addWidget(self.all_users)
            return
        
        # fill in the user's information
        for user in master_users:
            hbox = QHBoxLayout()
            
            # fill in the user's username
            name = QLabel('Username:')
            name.setProperty('class', 'small-bold-label')
            hbox.addWidget(name)
            n = QLabel(user[0])    # TODO pass correct index into user[x]
            n.setProperty('class', 'small-tab-info')
            hbox.addWidget(n)
            
            # fill in the user's email
            email = QLabel('E-Mail:')
            email.setProperty('class', 'small-bold-label')
            hbox.addWidget(email)
            l = QLabel(user[1])    # TODO pass correct index into user[x]
            l.setProperty('class', 'small-tab-info')
            hbox.addWidget(l)
            
            # fill in the user's total hours
            hours = QLabel('Volunteer Hours:')
            hours.setProperty('class', 'small-bold-label')
            hbox.addWidget(hours)
            time = '%s' % (user[3])    # TODO pass correct index into user[x]
            t = QLabel(time)
            t.setProperty('class', 'small-tab-info')
            hbox.addWidget(t)
            
            # fill in the user's total donations
            money = QLabel('Total Donations:')
            money.setProperty('class', 'small-bold-label')
            hbox.addWidget(money)
            amount = '%s' % (user[2])    # TODO pass correct index into user[x]
            a = QLabel(amount)
            a.setProperty('class', 'small-tab-info')
            hbox.addWidget(a)
            
            # create the generate report button
            gen_rep_btn = QPushButton('Generate Report')
            gen_rep_btn.setProperty('class', 'normal-bar-btn')
            print(f'user[4] {user[4]}')
            gen_rep_btn.clicked.connect(partial(self.generate_single_user_report, user[4]))    # TODO pass correct index into user[x]
            gen_rep_btn.setCursor(QCursor(Qt.PointingHandCursor))
            
            # create the delete user button
            delete_btn = QPushButton('Delete User')
            delete_btn.setProperty('class', 'red-bar-btn')
            delete_btn.clicked.connect(partial(self.delete_user, user[4]))
            delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
            
            # add the buttons to the HBox
            hbox.addWidget(gen_rep_btn)
            hbox.addWidget(delete_btn)
            
            # set up the layouts
            hbox_2 = QHBoxLayout()
            spacer = QLabel("")
            spacer.setProperty('class', 'upcoming-label')
            hbox_2.addWidget(spacer)
            
            self.all_users_vbox.addLayout(hbox)
            self.all_users_vbox.addLayout(hbox_2)
        
        # add the scroll area to the VBox
        self.vbox_1.addWidget(self.all_users)
    
    # populate all events
    def populate_all_events(self):
        # Build the scroll areas
        self.all_events_widget = QWidget()
        self.all_events_vbox = QVBoxLayout()
        self.all_events_widget.setLayout(self.all_events_vbox)
        self.all_events = QScrollArea()
        self.all_events.setWidget(self.all_events_widget)
        self.all_events.setWidgetResizable(True)
        self.all_events.setFixedHeight(575)
        sys_width, sys_height = self.screen_resolution()
        self.all_events.setFixedWidth((sys_width // 2) - 35)
        self.all_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # TODO fill event scroll area with proper information
        try:
            ids = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
        except:
            ids = "-1"
        
        # if the user is not signed up for any events
        if ids == '-1':
            hbox = QHBoxLayout()
            no_events = QLabel('No events have been scheduled by the organization.')
            no_events.setAlignment(Qt.AlignCenter)
            no_events.setProperty('class', 'no-events-label')
            hbox.addWidget(no_events)
            self.all_events_vbox.addLayout(hbox)
            self.vbox_2.addWidget(self.all_events)
            return
        
        # holds event ids from database
        event_ids = ids.split(' ')
        
        # master list to hold all events
        master_events = []
        
        # build up all event data
        for id in event_ids:
            event = Event.get(Event.id == id)
            
            # retrieve all relevant information
            master_events.append([event.name,
                                  event.location,
                                  event.month,
                                  event.day,
                                  event.year,
                                  event.start_date,
                                  event.end_date,
                                  id])
        
        # set the current date and time
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year
        self.currentDay = datetime.now().day
        
        # filter out events that have already passed and sort the events by date
        master_events = [event for event in master_events if not int(event[4]) < self.currentYear]
        master_events = [event for event in master_events if not ((int(event[2]) < self.currentMonth) and
                                                                  (int(event[4]) <= self.currentYear))]
        master_events = [event for event in master_events if not ((int(event[3]) < self.currentDay) and
                                                                  (int(event[2]) <= self.currentMonth))]
        master_events.sort(key=lambda x: (int(x[4]), int(x[2]), int(x[3]), x[5]))
        
        # if there are no events the user has signed up for
        if len(master_events) == 0:
            # inform the user that no events have been scheduled yet
            hbox = QHBoxLayout()
            no_events = QLabel('No events have been scheduled by the organization.')
            no_events.setAlignment(Qt.AlignCenter)
            no_events.setProperty('class', 'no-events-label')
            hbox.addWidget(no_events)
            self.all_events_vbox.addLayout(hbox)
            self.vbox_2.addWidget(self.all_events)
            return
        
        # fill in the user's upcoming events
        for event in master_events:
            hbox = QHBoxLayout()
            
            # fill in the event name
            name = QLabel('Name:')
            name.setProperty('class', 'small-bold-label')
            hbox.addWidget(name)
            n = QLabel(event[0])
            n.setProperty('class', 'small-tab-info')
            hbox.addWidget(n)
            
            # fill in the event location
            location = QLabel('Location:')
            location.setProperty('class', 'small-bold-label')
            hbox.addWidget(location)
            l = QLabel(event[1])
            l.setProperty('class', 'small-tab-info')
            hbox.addWidget(l)
            
            # fill in the event date
            date = QLabel('Date:')
            date.setProperty('class', 'small-bold-label')
            hbox.addWidget(date)
            time = '%s/%s/%s, %s-%s' % (event[2], event[3], event[4], event[5], event[6])
            t = QLabel(time)
            t.setProperty('class', 'small-tab-info')
            hbox.addWidget(t)
            
            # create the cancel event button
            delete_btn = QPushButton('Delete Event')
            delete_btn.setProperty('class', 'red-bar-btn')
            delete_btn.clicked.connect(partial(self.delete_event, event[7]))
            delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
            
            # add the buttons to the HBox
            hbox.addWidget(delete_btn)
            
            # set up the layouts
            hbox_2 = QHBoxLayout()
            spacer = QLabel("")
            spacer.setProperty('class', 'upcoming-label')
            hbox_2.addWidget(spacer)
            
            self.all_events_vbox.addLayout(hbox)
            self.all_events_vbox.addLayout(hbox_2)
        
        # add the scroll area to the VBox
        self.vbox_2.addWidget(self.all_events)
    
    # hides the previous items from view
    def hide_previous(self):
        # hide the scrollboxes
        self.all_users.hide()
        self.all_events.hide()
    
    # delete a user. This will update the User and Event tables.
    def delete_user(self, user_id):
        # TODO finish this
        
        # Note: these should be the very last three lines of this method
        QMessageBox.warning(self, " ", "The user has been successfully deleted.")
        self.hide_previous()         # empty users and events
        self.populate_all_users()    # repopulate users
        self.populate_all_events()   # repopulate events
    
    # delete a volunteering event. This will update the User and Event tables.
    def delete_event(self, event_id):
        # TODO this entire method needs to be changed
        # remove the event from the user list
        user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
        event_ids = user_events.split(' ')
        event_ids.remove(str(event_id))
        event_ids = ' '.join(event_ids)
        
        # Update users volunteer hours
        s_time = Event.get(Event.id == event_id).start_date
        e_time = Event.get(Event.id == event_id).end_date
        self.update_all_volunteer_hours(s_time, e_time)
        
        # The user has no events left, so reset it to the value for no events
        if event_ids == '':
            event_ids = '-1'
        
        # Update the users new events. Remove the user from the event and decrement the volunteer count
        User.update({User.event_ids: event_ids}).where(User.user_id == cs.CURRENT_USER_ID).execute()
        volunteer_ids = Event.get(Event.id == event_id).volunteers_ids
        volunteer_count = Event.get(Event.id == event_id).volunteers_attending
        volunteer_count -= 1
        # print(f'volunteers here {volunteer_ids} volunteer count {volunteer_count}')
        # No volunteers, reset the id to -1
        if volunteer_count == 0:
            volunteer_ids = '-1'
        
        # Update the new volunteer count and volunteers
        # print(f'volunteer when updating {volunteer_ids} num {volunteer_count}')
        Event.update({Event.volunteers_attending: volunteer_count}).where(Event.id == event_id).execute()
        Event.update({Event.volunteers_ids: volunteer_ids}).where(Event.id == event_id).execute()
        QMessageBox.warning(self, " ", "The event has been successfully deleted.")
        self.hide_previous()         # empty users and events
        self.populate_all_users()    # repopulate users
        self.populate_all_events()   # repopulate events
    
    # after an event is deleted, updates all volunteer hours
    def update_all_volunteer_hours(self, start_time, end_time):
        # TODO finish this
        pass
    
    # after a user is deleted, updates all events they were registered for
    def update_all_event_volunteers(self, user_id):
        # TODO finish this
        pass
    
    # generates a report on a single user
    def generate_single_user_report(self, user_id):
        # TODO finish this: It should write a text file out to an output directory with user information
        #                   such as their username, email, total hours volunteered by the user, and total
        #                   money donated by the user.

        user = User.get(User.user_id == user_id)
        # TODO user info can now be found by using user.user_id or user.username or whatever field is needed

    # generates a report on all users
    def generate_all_users_report(self):
        # TODO finish this: It should write a text file out to an output directory with all user information
        #                   such as total hours volunteered by all users, total money donated by all users.

        users = User.select()
        for user in users:
            # TODO you have access to each user here. So you can do user.username, user.account_email, etc.
            pass

    # generates a report on organization and all events
    def generate_all_events_report(self):
        # TODO finish this: It should write a text file out to an output directory with all event information
        #                   such as total hours all events add up to, total donations to events, and total
        #                   donations to the organization
        org = OrgEvent.get(OrgEvent.id == cs.ORG_ID)
        print('ZIB')
        # total org donations is just org.donations
        try:
            events = Event.select()
        except Event.DoesNotExist:
            events = None
        # TODO write the org information to the file first, because there will always be org but there can be zero event
        #  ->
        if events is None:
            return
        # TODO write event information, you have the information for each event
        total_event_hours = 0.0
        total_event_donations = 0
        for event in events:
            total_event_donations += event.donations
            total_event_hours += self.get_event_runtime(event)
            print(f'event information: name {event.name} location {event.location} event')
        print(f'total event hours {total_event_hours} total event donations {total_event_donations}')

    # helper method to determine the length of an event
    def get_event_runtime(self, event):
        s_time = event.start_date
        e_time = event.end_date
        start = s_time.split(':')
        end = e_time.split(':')
        if start[1] == '30':
            s_min = 0.5
        else:
            s_min = 0.0
        if end[1] == '30':
            e_min = 0.5
        else:
            e_min = 0.0
        end_total = float(end[0]) + e_min
        start_total = float(start[0]) + s_min
        return end_total - start_total

    # creates the layout for the bar of tabs at the top of the application
    def top_bar(self):
        # set up the home button
        self.home_btn = QPushButton("Home")
        self.home_btn.clicked.connect(self.home_click)
        self.home_btn.setProperty('class', 'normal-bar-btn')
        self.home_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the calendar button
        self.cal_btn = QPushButton("Calendar")
        self.cal_btn.clicked.connect(self.cal_click)
        self.cal_btn.setProperty('class', 'normal-bar-btn')
        self.cal_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the about us button
        self.about_btn = QPushButton("About Us")
        self.about_btn.clicked.connect(self.about_click)
        self.about_btn.setProperty('class', 'normal-bar-btn')
        self.about_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the contact us button
        self.contact_btn = QPushButton("Contact Us")
        self.contact_btn.clicked.connect(self.contact_click)
        self.contact_btn.setProperty('class', 'normal-bar-btn')
        self.contact_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the help button
        self.help_btn = QPushButton("Help")
        self.help_btn.clicked.connect(self.help_click)
        self.help_btn.setProperty('class', 'normal-bar-btn')
        self.help_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_click)
        self.search_btn.setProperty('class', 'normal-bar-btn')
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the account button (if the user is logged in)
        self.account_btn = QPushButton("Account")
        self.account_btn.clicked.connect(self.account_click)
        self.account_btn.setProperty('class', 'special-bar-btn')
        self.account_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the log out button (if the user is logged in)
        self.logout_btn = QPushButton("Log Out")
        self.logout_btn.clicked.connect(self.logout_click)
        self.logout_btn.setProperty('class', 'special-bar-btn')
        self.logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the sign up button (if the user is logged out)
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.signup_click)
        self.signup_btn.setProperty('class', 'special-bar-btn')
        self.signup_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the log in button (if the user is logged out)
        self.login_btn = QPushButton("Log In")
        self.login_btn.clicked.connect(self.login_click)
        self.login_btn.setProperty('class', 'special-bar-btn')
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # define the HBox
        self.hbox_bar = QHBoxLayout()
        
        # add all buttons to the HBox
        self.hbox_bar.addWidget(self.home_btn)
        self.hbox_bar.addWidget(self.cal_btn)
        self.hbox_bar.addWidget(self.about_btn)
        self.hbox_bar.addWidget(self.contact_btn)
        self.hbox_bar.addWidget(self.help_btn)
        self.hbox_bar.addWidget(self.search_btn)
        self.hbox_bar.addWidget(QLabel(""))
        self.hbox_bar.addWidget(self.account_btn)
        self.hbox_bar.addWidget(self.logout_btn)
        self.hbox_bar.addWidget(self.signup_btn)
        self.hbox_bar.addWidget(self.login_btn)
        
        # check which type of user is logged in to determine what buttons will show up
        self.check_user()
        
        # add the HBox to the VBox
        self.vbox_screen.addLayout(self.hbox_bar)
    
    # go to the homepage
    def home_click(self):
        self.win.set_page(self.this_page, cs.PAGE_HOME)
    
    # go to the calendar page
    def cal_click(self):
        self.win.set_page(self.this_page, cs.PAGE_CAL)
    
    # go to the about us page
    def about_click(self):
        self.win.set_page(self.this_page, cs.PAGE_ABOUT)
    
    # go to the contact us page
    def contact_click(self):
        self.win.set_page(self.this_page, cs.PAGE_CONTACT)
    
    # go to the help page
    def help_click(self):
        self.win.set_page(self.this_page, cs.PAGE_HELP)
    
    # go to the search page
    def search_click(self):
        self.win.set_page(self.this_page, cs.PAGE_SEARCH)
    
    # go to the account page
    def account_click(self):
        self.win.set_page(self.this_page, cs.PAGE_ACCOUNT)
    
    # return to the login signup screen
    def logout_click(self):
        self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
        
        cs.CURRENT_USER = "Guest"
    
    # go to the login page
    def login_click(self):
        self.win.set_page(self.this_page, cs.PAGE_LOGIN)
    
    # go to the new account page
    def signup_click(self):
        self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
    
    # go to the administrator priveleges page
    def admin_privileges(self):
        self.win.set_page(self.this_page, cs.PAGE_PRIVILEGES)
    
    # draws shapes on the window
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # retrieve the resolution of the system
        sys_width, sys_height = self.screen_resolution()
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(0, 127, sys_width, 60)
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(0, 250, (sys_width // 2) - 5, 675)
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect((sys_width // 2) + 5, 250, (sys_width // 2) - 5, 675)
    
    # resets the coordinates of the window after switching to this page
    def set_position(self):
        self.parent().move(self.x_coord, self.y_coord)
        self.parent().resize(self.width, self.height)
    
    # checks which user is logged in and formats the page to accomodate the user type
    def check_user(self):
        # check if the current user is a guest
        if cs.CURRENT_USER == "Guest":
            # show the signup and login buttons
            self.signup_btn.show()
            self.login_btn.show()
            
            # hide the account and logout buttons
            self.account_btn.hide()
            self.logout_btn.hide()
        
        # if the current user is not a guest
        else:
            # hide the signup and login buttons
            self.signup_btn.hide()
            self.login_btn.hide()
            
            # show the account and logout buttons
            self.account_btn.show()
            self.logout_btn.show()
        
        # check if the current user is a volunteer
        if cs.CURRENT_USER == "Volunteer":
            pass
        
        # check if the current user is a staff member
        if cs.CURRENT_USER == "Staff":
            pass
        
        # check if the current user is an administrator
        if cs.CURRENT_USER == "Administrator":
            pass
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)
        
        return geometry.width(), geometry.height()
