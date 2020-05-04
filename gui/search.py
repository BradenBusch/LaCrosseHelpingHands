'''
Search page of the application, allows users to search for other users and events.

Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/23/2020

'''

from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit.models.database import *
    from non_profit import constants as cs
except:
    from models.database import *
    import constants as cs


class Search(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'search')
        self.setWindowTitle("Search")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_SEARCH
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        self.vbox_screen = QVBoxLayout()
        
        self.hbox_1 = QHBoxLayout()
        self.spacer_1 = QLabel("")
        self.spacer_1.setProperty('class', 'search-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)
        
        # create the top bar of tabs for the application
        self.top_bar()
        
        # create HBoxes
        self.hbox_2 = QHBoxLayout()
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        
        # create the VBox
        self.hbox_screen = QHBoxLayout()
        
        self.search_label = QLabel("Search")
        self.search_label.setProperty('class', 'cal-label')
        self.search_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.search_label)
        
        # retrieve system dimensions
        sys_width, sys_height = self.screen_resolution()
        
        # create the search bar
        self.search_bar = QLineEdit()
        self.search_bar.setMaxLength(50)
        self.search_bar.setFixedWidth(sys_width // 4)
        self.search_bar.setPlaceholderText("Enter search query")
        
        # create the search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.populate_results)
        self.search_btn.setProperty('class', 'special-bar-btn')
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # add search bar and search button to the layout
        self.hbox_3.addWidget(self.search_bar)
        self.hbox_3.addWidget(self.search_btn)
        self.hbox_3.setAlignment(Qt.AlignLeft)
        
        # create results label
        self.results_label = QLabel("")
        self.results_label.setProperty('class', 'bold-label')
        
        # add results label to the layout
        self.hbox_4.addWidget(self.results_label)
        
        # add HBoxes to top level VBox
        self.vbox_screen.addLayout(self.hbox_2)
        self.vbox_screen.addLayout(self.hbox_3)
        self.vbox_screen.addLayout(self.hbox_4)
        self.vbox_screen.addLayout(self.hbox_screen)
        
        # populate scroll area with results
        self.populate_results()
        
        # create spacer for bottom of screen
        self.hbox_5 = QHBoxLayout()
        self.spacer_2 = QLabel("")
        self.spacer_2.setProperty('class', 'search-bottom-spacer-label')
        self.hbox_5.addWidget(self.spacer_2)
        self.vbox_screen.addLayout(self.hbox_5)
        
        # set up the layout
        self.setLayout(self.vbox_screen)
        
        # set the geometry of the window
        self.x_coord = 0
        self.y_coord = 40
        self.width = sys_width
        self.height = sys_height
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # populate a scrollbox with all of the upcoming events
    def populate_results(self):
        try:
            self.results.hide()
        except:
            pass
        
        # holds the search query
        query = self.search_bar.text()
        
        # if the user did not enter anything
        if query == "":
            self.results_label.setText("Please enter a search query.")
        else:
            self.results_label.setText("Search results for '{}':".format(query))
            self.search_bar.clear()
        
        # create the scrollbox
        self.results_widget = QWidget()
        self.results_vbox = QVBoxLayout()
        self.results_widget.setLayout(self.results_vbox)
        self.results = QScrollArea()
        self.results.setWidget(self.results_widget)
        self.results.setWidgetResizable(True)
        self.results.setFixedHeight(575)
        sys_width, sys_height = self.screen_resolution()
        self.results.setFixedWidth(sys_width - 20)
        self.results.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # if the user has not made a search yet
        if query == "":
            hbox = QHBoxLayout()
            no_results = QLabel('Search across all of our users and events.')
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setProperty('class', 'no-events-label')
            hbox.addWidget(no_results)
            self.results_vbox.addLayout(hbox)
            self.hbox_screen.addWidget(self.results)
            return
        
        # attempt to retrieve events from the database
        try:
            events = Event.select()
        except:
            events = []
        
        # master list to hold all events
        master_events = []
        
        # build up all event data
        for e in events:
            event = Event.get(Event.id == e.id)
            
            # retrieve all relevant information
            master_events.append([event.name,
                                  event.location,
                                  event.month,
                                  event.day,
                                  event.year,
                                  event.start_date,
                                  event.end_date])
        
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
        
        # filter out all events that do not match the search query
        master_events = [event for event in master_events if ((query in event[0]) or (query in event[1]))]
        
        # attempt to retrieve users from the database
        try:
            users = User.select()
        except:
            users = []
        
        # master list to hold all users
        master_users = []
        
        # build up all user data
        for user in users:
            # retrieve all relevant information
            master_users.append([user.username,
                                 user.account_email,
                                 user.total_donations,
                                 user.volunteer_hours,
                                 user.user_id,
                                 user.valid,
                                 user.account_type])
        
        # sort the users alphabetically by username
        master_users.sort(key=lambda x: x[0])
        
        # filter out all users that do not match the search query
        master_users = [user for user in master_users if ((query in user[0]) or
                                                          (query in user[1]) or
                                                          (query in user[6]))]
        
        # if there are no search results for the user's query
        if len(master_events) == 0 and len(master_users) == 0:
            # inform the user that no results were found
            hbox = QHBoxLayout()
            no_results = QLabel('No results match that query.')
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setProperty('class', 'no-events-label')
            hbox.addWidget(no_results)
            self.results_vbox.addLayout(hbox)
            self.hbox_screen.addWidget(self.results)
            return
        
        # fill in the events form
        for event in master_events:
            hbox = QHBoxLayout()

            # indicate what type of result this is
            result_type = QLabel('EVENT')
            result_type.setProperty('class', 'bold-label')
            hbox.addWidget(result_type)
            
            # fill in the event name
            name = QLabel('Name:')
            name.setProperty('class', 'bold-label')
            hbox.addWidget(name)
            n = QLabel(event[0])
            n.setProperty('class', 'tab-info')
            hbox.addWidget(n)
            
            # fill in the event location
            location = QLabel('Location:')
            location.setProperty('class', 'bold-label')
            hbox.addWidget(location)
            l = QLabel(event[1])
            l.setProperty('class', 'tab-info')
            hbox.addWidget(l)
            
            # fill in the event date
            date = QLabel('Date:')
            date.setProperty('class', 'bold-label')
            hbox.addWidget(date)
            time = '%s/%s/%s, %s-%s' % (event[2], event[3], event[4], event[5], event[6])
            t = QLabel(time)
            t.setProperty('class', 'tab-info')
            hbox.addWidget(t)
            
            # set up the layouts
            hbox_2 = QHBoxLayout()
            spacer = QLabel("")
            spacer.setProperty('class', 'upcoming-label')
            hbox_2.addWidget(spacer)
            
            self.results_vbox.addLayout(hbox)
            self.results_vbox.addLayout(hbox_2)
        
        # fill in the user's information
        for user in master_users:
            hbox = QHBoxLayout()
            
            # indicate what type of result this is
            result_type = QLabel('USER')
            result_type.setProperty('class', 'bold-label')
            hbox.addWidget(result_type)
            
            # fill in the user's username
            name = QLabel('Username:')
            name.setProperty('class', 'bold-label')
            hbox.addWidget(name)
            n = QLabel(user[0])
            n.setProperty('class', 'tab-info')
            hbox.addWidget(n)
            
            # fill in the user's email
            email = QLabel('E-Mail:')
            email.setProperty('class', 'bold-label')
            hbox.addWidget(email)
            l = QLabel(user[1])
            l.setProperty('class', 'tab-info')
            hbox.addWidget(l)
            
            # fill in the user's total hours
            hours = QLabel('Volunteer Hours:')
            hours.setProperty('class', 'bold-label')
            hbox.addWidget(hours)
            time = '%s' % (user[3])
            t = QLabel(time)
            t.setProperty('class', 'tab-info')
            hbox.addWidget(t)
            
            # fill in the user's account type
            account_type = QLabel('Account Type:')
            account_type.setProperty('class', 'bold-label')
            hbox.addWidget(account_type)
            acc = QLabel(user[6])
            acc.setProperty('class', 'tab-info')
            hbox.addWidget(acc)
            
            # fill in the user's total donations
            # money = QLabel('Total Donations:')
            # money.setProperty('class', 'bold-label')
            # hbox.addWidget(money)
            # amount = '%s' % (user[2])
            # a = QLabel(amount)
            # a.setProperty('class', 'tab-info')
            # hbox.addWidget(a)
    
            # set up the layouts
            hbox_2 = QHBoxLayout()
            spacer = QLabel("")
            spacer.setProperty('class', 'upcoming-label')
            hbox_2.addWidget(spacer)

            self.results_vbox.addLayout(hbox)
            self.results_vbox.addLayout(hbox_2)
        
        # add the scroll area to the VBox
        self.hbox_screen.addWidget(self.results)
    
    # hides the previous items from view
    def hide_previous(self):
        # hide the scrollbox
        self.results.hide()
    
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
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_HOME)
    
    # go to the calendar page
    def cal_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_CAL)
    
    # go to the about us page
    def about_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_ABOUT)
    
    # go to the contact us page
    def contact_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_CONTACT)
    
    # go to the help page
    def help_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_HELP)
    
    # go to the search page
    def search_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_SEARCH)
    
    # go to the account page
    def account_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_ACCOUNT)
    
    # return to the login signup screen
    def logout_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
        
        cs.CURRENT_USER = "Guest"
    
    # go to the login page
    def login_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_LOGIN)
    
    # go to the new account page
    def signup_click(self):
        self.search_bar.clear()
        self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
    
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
        painter.drawRect(0, 250, sys_width, 675)
    
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
