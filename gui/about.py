'''
About page of the application, describes the organization to the user.

Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/23/2020

'''

import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit import constants as cs
except:
    import constants as cs


class About(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'about')
        self.setWindowTitle("About Us")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_ABOUT
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        self.vbox_screen = QVBoxLayout()
        
        self.hbox_1 = QHBoxLayout()
        self.spacer_1 = QLabel("")
        self.spacer_1.setProperty('class', 'about-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)
        
        # create the top bar of tabs for the application
        self.top_bar()
        
        # create HBoxes
        self.hbox_2 = QHBoxLayout()
        self.hbox_screen = QHBoxLayout()
        
        self.about_label = QLabel("About Us")
        self.about_label.setProperty('class', 'cal-label')
        self.about_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.about_label)
        
        # Divide the screen into halves
        self.vbox_1 = QVBoxLayout()
        self.vbox_2 = QVBoxLayout()
        
        self.about_desc_1 = QLabel("Who We Are")
        self.about_desc_1.setProperty('class', 'bold-under-label')
        self.about_desc_1.setWordWrap(True)
        self.vbox_1.addWidget(self.about_desc_1)
        
        self.about_desc_2 = QLabel("We are concerned citizens of the La Crosse area working to alleviate " + \
                                   "the hardships experienced by the underserved populations of the La Crosse area." + \
                                   "  We are made up of a small number of Administrators and Staff while the rest " + \
                                   "of our organization is made up of Volunteers like you!")
        self.about_desc_2.setProperty('class', 'acc-desc-label')
        self.about_desc_2.setWordWrap(True)
        self.vbox_1.addWidget(self.about_desc_2)
        
        self.about_desc_3 = QLabel("What We Do")
        self.about_desc_3.setProperty('class', 'bold-under-label')
        self.vbox_1.addWidget(self.about_desc_3)
        
        self.about_desc_4 = QLabel("We are a non-profit organization that provides food, medical care, and other " + \
                                   "services to those individuals who are" + \
                                   " unable to acquire it themselves. If you know of a way we can help near you, " + \
                                   "feel free to visit our Contact Us page and let us know!")
        self.about_desc_4.setProperty('class', 'acc-desc-label')
        self.about_desc_4.setWordWrap(True)
        self.vbox_1.addWidget(self.about_desc_4)
        
        self.about_desc_5 = QLabel("Our Goals")
        self.about_desc_5.setProperty('class', 'bold-under-label')
        self.vbox_1.addWidget(self.about_desc_5)
        
        self.about_desc_6 = QLabel("Our goals are simple.  Help in any way we can and make sure everyone " + \
                                   "gets the proper care they need.  It's often the most hurt individuals " + \
                                   "in our society that need the most care.  Become a Volunteer today, you " + \
                                   "can even make a charitable donation to our organization to help with our " + \
                                   "funding!")
        self.about_desc_6.setProperty('class', 'acc-desc-label')
        self.about_desc_6.setWordWrap(True)
        self.vbox_1.addWidget(self.about_desc_6)
        
        # create labels for the information
        self.image_title = QLabel("Working For You")
        self.image_title.setProperty('class', 'home-events-label')
        self.image_title.setFixedHeight(40)
        self.image_title.setAlignment(Qt.AlignCenter)
        self.vbox_2.addWidget(self.image_title)
        
        # retrieve system resolution
        sys_width, sys_height = self.screen_resolution()
        
        # set up the image
        self.about_image = QLabel(self)
        
        # if file exists else use the other one (handles path to the image)
        if os.path.isfile('gui\\photos\\about.png'):
            pixmap = QPixmap('gui\\photos\\about.png')
        else:
            pixmap = QPixmap('non_profit\\gui\\photos\\about.png')
        
        # set width and height of image
        scaled_height = int(pixmap.height() * ((sys_width // 2) / pixmap.width()))
        pixmap = pixmap.scaled((sys_width // 2), scaled_height, transformMode=Qt.SmoothTransformation)
        self.about_image.setPixmap(pixmap)
        self.about_image.resize(pixmap.width(), pixmap.height())
        self.vbox_2.addWidget(self.about_image)
        
        # add two VBoxes to top level HBox
        self.hbox_screen.addLayout(self.vbox_1)
        self.hbox_screen.addLayout(self.vbox_2)
        
        # add HBoxes to top level VBox
        self.vbox_screen.addLayout(self.hbox_2)
        self.vbox_screen.addLayout(self.hbox_screen)
        
        # create spacer for bottom of screen
        self.hbox_3 = QHBoxLayout()
        self.spacer_2 = QLabel("")
        self.spacer_2.setProperty('class', 'about-bottom-spacer-label')
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
