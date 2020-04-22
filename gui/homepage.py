'''
Homepage of the application, all users are directed here after logging in.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/21/2020

'''

import os
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


class Homepage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'homepage')
        self.setWindowTitle("Welcome!")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_HOME
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        self.vbox_screen = QVBoxLayout()
        
        self.hbox_1 = QHBoxLayout()
        self.spacer_1 = QLabel("")
        self.spacer_1.setProperty('class', 'home-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)
        
        # create the my events button, to be used below
        self.my_events_btn = QPushButton("View My Events")
        
        # create the top bar of tabs for the application
        self.top_bar()
        
        # create HBoxes
        self.hbox_2 = QHBoxLayout()
        self.hbox_screen = QHBoxLayout()
        
        self.welcome_label = QLabel("Welcome!")
        self.welcome_label.setProperty('class', 'cal-label')
        self.welcome_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.welcome_label)
        
        # Divide the screen into halves
        self.vbox_1 = QVBoxLayout()
        self.vbox_2 = QVBoxLayout()
        
        # set the paragraph of text to display above the picture
        self.home_desc_1 = QLabel(self.get_text("home_description.txt"))
        self.home_desc_1.setProperty('class', 'home-desc-label')
        self.home_desc_1.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_1)
        
        self.home_desc_2 = QLabel("Interested in volunteering at one of our events and making your mark in the La Crosse community?")
        self.home_desc_2.setProperty('class', 'bold-text-label')
        self.home_desc_2.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_2)
        
        self.home_desc_3 = QLabel("• Register an account and head over to our Calendar page to register for events!")
        self.home_desc_3.setProperty('class', 'home-desc-label')
        self.home_desc_3.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_3)
        
        self.home_desc_4 = QLabel("Interested in making a donation to our organization?")
        self.home_desc_4.setProperty('class', 'bold-text-label')
        self.home_desc_4.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_4)
        
        self.home_desc_5 = QLabel("• Register an account and donate to your heart's content!")
        self.home_desc_5.setProperty('class', 'home-desc-label')
        self.home_desc_5.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_5)
        
        self.home_desc_6 = QLabel("Interested in joining our staff or administrator team?")
        self.home_desc_6.setProperty('class', 'bold-text-label')
        self.home_desc_6.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_6)
        
        self.home_desc_7 = QLabel("• Visit the Contact Us page and contact us directly, we'd be delighted to have you join us!")
        self.home_desc_7.setProperty('class', 'home-desc-label')
        self.home_desc_7.setWordWrap(True)
        self.vbox_1.addWidget(self.home_desc_7)
        
        # retrieve system resolution
        sys_width, sys_height = self.screen_resolution()
        
        # set up the image
        self.hands_image = QLabel(self)
        
        # if file exists else use the other one (handles path to the image)
        if os.path.isfile('gui\\photos\\homepage.png'):
            pixmap = QPixmap('gui\\photos\\homepage.png')
        else:
            pixmap = QPixmap('non_profit\\gui\\photos\\homepage.png')
        
        # set width and height of image
        scaled_height = int(pixmap.height() * ((sys_width // 2) / pixmap.width()))
        pixmap = pixmap.scaled((sys_width // 2), scaled_height, transformMode=Qt.SmoothTransformation)
        self.hands_image.setPixmap(pixmap)
        self.hands_image.resize(pixmap.width(), pixmap.height())
        self.vbox_1.addWidget(self.hands_image)
        
        # create labels for the information
        self.events_label = QLabel("Upcoming Events")
        self.events_label.setProperty('class', 'home-events-label')
        self.events_label.setFixedHeight(40)
        self.events_label.setAlignment(Qt.AlignCenter)
        self.vbox_2.addWidget(self.events_label)
        
        # populate scroll area with upcoming events
        self.populate_all_events()
        self.my_events_btn.clicked.connect(self.account_click)
        self.my_events_btn.setProperty('class', 'special-bar-btn')
        self.my_events_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # this hbox is just so we can center the button
        self.center_hbox = QHBoxLayout()
        self.center_hbox.setAlignment(Qt.AlignCenter)
        self.center_hbox.addWidget(self.my_events_btn)
        self.vbox_2.addLayout(self.center_hbox)
        
        # add two VBoxes to top level HBox
        self.hbox_screen.addLayout(self.vbox_1)
        self.hbox_screen.addLayout(self.vbox_2)
        
        # add HBoxes to top level VBox
        self.vbox_screen.addLayout(self.hbox_2)
        self.vbox_screen.addLayout(self.hbox_screen)
        
        # create spacer for bottom of screen
        self.hbox_3 = QHBoxLayout()
        self.spacer_2 = QLabel("")
        self.spacer_2.setProperty('class', 'home-bottom-spacer-label')
        self.hbox_3.addWidget(self.spacer_2)
        self.vbox_screen.addLayout(self.hbox_3)
        
        # set up the layout
        self.setLayout(self.vbox_screen)
        
        # set the geometry of the window
        self.x_coord = 0
        self.y_coord = 40
        self.width = sys_width
        self.height = sys_height
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # populate a scrollbox with all of the upcoming events
    def populate_all_events(self):
        # create the scrollbox
        self.all_events_widget = QWidget()
        self.all_events_vbox = QVBoxLayout()
        self.all_events_widget.setLayout(self.all_events_vbox)
        self.all_events = QScrollArea()
        self.all_events.setWidget(self.all_events_widget)
        self.all_events.setWidgetResizable(True)
        self.all_events.setFixedHeight(500)
        sys_width, sys_height = self.screen_resolution()
        self.all_events.setFixedWidth((sys_width // 2) - 35)
        self.all_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # attempt to retrieve events from the database
        try:
            events = Event.select()
        except Event.DoesNotExist:
            return
        
        # if there are no events yet
        if len(events) == 0:
            # inform the user that no events have been scheduled yet
            hbox = QHBoxLayout()
            no_events = QLabel('No upcoming events have been scheduled by the organization!')
            no_events.setAlignment(Qt.AlignCenter)
            no_events.setProperty('class', 'no-events-label')
            hbox.addWidget(no_events)
            self.all_events_vbox.addLayout(hbox)
            self.vbox_2.addWidget(self.all_events)
            return
        
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
        
        # if there are no events yet
        if len(master_events) == 0:
            # inform the user that no events have been scheduled yet
            hbox = QHBoxLayout()
            no_events = QLabel('No upcoming events have been scheduled by the organization!')
            no_events.setAlignment(Qt.AlignCenter)
            no_events.setProperty('class', 'no-events-label')
            hbox.addWidget(no_events)
            self.all_events_vbox.addLayout(hbox)
            self.vbox_2.addWidget(self.all_events)
            return
        
        # fill in the upcoming events form
        for event in master_events:
            hbox = QHBoxLayout()
            
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
            
            self.all_events_vbox.addLayout(hbox)
            self.all_events_vbox.addLayout(hbox_2)
        
        # add the scroll area to the VBox
        self.vbox_2.addWidget(self.all_events)
    
    # hides the previous items from view
    def hide_previous(self, thing_to_hide):
        # check which item to hide
        if thing_to_hide == 1:
            # hide the scrollbox
            self.all_events.hide()
        elif thing_to_hide == 2:
            # hide the button
            self.my_events_btn.hide()
            
            # recreate the my events button
            self.my_events_btn = QPushButton("View My Events")
            self.my_events_btn.clicked.connect(self.account_click)
            self.my_events_btn.setProperty('class', 'special-bar-btn')
            self.my_events_btn.setCursor(QCursor(Qt.PointingHandCursor))
            
            # recreate the center HBox
            self.center_hbox = QHBoxLayout()
            self.center_hbox.setAlignment(Qt.AlignCenter)
            self.center_hbox.addWidget(self.my_events_btn)
            self.vbox_2.addLayout(self.center_hbox)
            
            # check which type of user is logged in to determine what buttons will show up
            self.check_user()
    
    # reads in all text from a passed .txt file and returns it as a string
    def get_text(self, filename):
        # if file exists else use the other one (handles path to the image)
        if os.path.isfile('gui\\text\\{}'.format(filename)):
            path = 'gui\\text\\{}'.format(filename)
        else:
            path = 'non_profit\\gui\\text\\{}'.format(filename)
        
        # open the file and read in all text
        with open(path, 'r') as text_file:
            text = text_file.read()
        
        return text
    
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
        
        # TODO actually log the user out of their account
        cs.CURRENT_USER = "Guest"
    
    # go to the login page
    def login_click(self):
        self.win.set_page(self.this_page, cs.PAGE_LOGIN)
    
    # go to the new account page
    def signup_click(self):
        self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
    
    # TODO add additional button methods here
    
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
            
            # hide the my events button
            self.my_events_btn.hide()
        
        # if the current user is not a guest
        else:
            # hide the signup and login buttons
            self.signup_btn.hide()
            self.login_btn.hide()
        
            # show the account and logout buttons
            self.account_btn.show()
            self.logout_btn.show()
            
            # show the my events button
            self.my_events_btn.show()
        
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
