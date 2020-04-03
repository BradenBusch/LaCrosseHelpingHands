'''
Window template, copy this file and rename it to create a new page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit.models.database import *
    from non_profit import constants as cs
except:
    from models.database import *
    import constants as cs


# TODO make the program not crash when a guest is logged in
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
        self.spacer_1.setProperty('class', 'cal-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)

        # create the top bar of tabs for the application
        self.top_bar()

        # create hbox's
        self.hbox_2 = QHBoxLayout()
        self.hbox_screen = QHBoxLayout()

        # create labels for the information
        self.all_events_label = QLabel("All Scheduled Events")
        self.all_events_label.setProperty('class', 'cal-label')
        self.all_events_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.all_events_label)

        self.user_events_label = QLabel("My Scheduled Events")
        self.user_events_label.setProperty('class', 'cal-label')
        self.user_events_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.user_events_label)

        # Divide the screen into halves
        self.vbox_1 = QVBoxLayout()
        self.vbox_2 = QVBoxLayout()

        # Add information to the vboxs TODO keep
        # self.my_events = QScrollArea()
        # self.my_events.setWidgetResizable(True)

        # TODO Make the scroll only take up half the page
        self.populate_all_events()
        self.show_events_btn = QPushButton("View My Events")
        self.show_events_btn.clicked.connect(self.populate_user_events)
        self.vbox_2.addWidget(self.show_events_btn)

        # Add two vboxes to top level hbox
        self.hbox_screen.addLayout(self.vbox_1)
        self.hbox_screen.addLayout(self.vbox_2)

        # Add hboxs to vbox
        self.vbox_screen.addLayout(self.hbox_2)
        self.vbox_screen.addLayout(self.hbox_screen)

        # create spacer for bottom of screen TODO REMOVE THIS?
        self.hbox_3 = QHBoxLayout()
        self.spacer_2 = QLabel("")
        self.spacer_2.setProperty('class', 'cal-bottom-spacer-label')
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

    def populate_all_events(self):
        self.all_events_widget = QWidget()
        self.all_events_vbox = QVBoxLayout()
        self.all_events_widget.setLayout(self.all_events_vbox)
        self.all_events = QScrollArea()
        self.all_events.setWidget(self.all_events_widget)
        self.all_events.setWidgetResizable(True)
        self.all_events.setFixedHeight(500)
        self.all_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # ids = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
        # event_ids = ids.split(' ')
        # print(f'ids {event_ids}')
        for id in range(100):
            # event = Event.get(Event.id == id)

            # v = QLabel(event.name)
            self.all_events_vbox.addWidget(QLabel('ficl'))
        self.vbox_1.addWidget(self.all_events)

    # Populate the users events
    def populate_user_events(self):
        # Hide the button
        self.show_events_btn.hide()

        # Build scroll area (its weird, i had to look up so much documentation)
        self.my_events_widget = QWidget()
        self.my_events_vbox = QVBoxLayout()
        self.my_events_widget.setLayout(self.my_events_vbox)
        self.my_events = QScrollArea()
        self.my_events.setWidget(self.my_events_widget)
        self.my_events.setWidgetResizable(True)
        self.my_events.setFixedHeight(600)  # TODO change this to how the calendar size was made
        self.my_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # print(f'cs.CURRENT_USER_ID: {cs.CURRENT_USER_ID}') TODO debug
        ids = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
        event_ids = ids.split(' ')
        # print(f'ids {event_ids}')
        for id in event_ids:
            event = Event.get(Event.id == id)
            hbox = QHBoxLayout()

            name = QLabel('Name: ')
            name.setProperty('class', 'bold-label')
            hbox.addWidget(name)
            n = QLabel(event.name)
            n.setProperty('class', 'tab-info')
            hbox.addWidget(n)

            location = QLabel('Location: ')
            location.setProperty('class', 'bold-label')
            hbox.addWidget(location)
            l = QLabel(event.location)
            l.setProperty('class', 'tab-info')
            hbox.addWidget(l)

            date = QLabel('Date: ')
            date.setProperty('class', 'bold-label')
            hbox.addWidget(date)
            time = '%s/%s/%s, %s-%s' % (event.month, event.day, event.year, event.start_date, event.end_date)
            t = QLabel(time)
            t.setProperty('class', 'tab-info')
            hbox.addWidget(t)

            cancel_btn = QPushButton('Cancel ' + str(event.name))
            cancel_btn.setProperty('class', 'normal-bar-btn')
            # cancel_btn.clicked.connect()
            hbox.addWidget(cancel_btn)
            self.my_events_vbox.addLayout(hbox)
        self.vbox_2.addWidget(self.my_events)

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
        # TODO add additional pages here
        self.hbox_bar.addWidget(self.about_btn)
        self.hbox_bar.addWidget(self.contact_btn)
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
