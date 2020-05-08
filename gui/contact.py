'''
Contact page of the application, describes how the user can contact the organization.

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


class Contact(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'contact')
        self.setWindowTitle("Contact Us")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_CONTACT
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        self.vbox_screen = QVBoxLayout()
        
        self.hbox_1 = QHBoxLayout()
        self.spacer_1 = QLabel("")
        self.spacer_1.setProperty('class', 'contact-bar-spacer-label')
        self.hbox_1.addWidget(self.spacer_1)
        self.vbox_screen.addLayout(self.hbox_1)
        
        # create the top bar of tabs for the application
        self.top_bar()
        
        # create HBoxes
        self.hbox_2 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.hbox_5 = QHBoxLayout()
        self.hbox_screen = QHBoxLayout()
        
        self.contact_label = QLabel("Contact Us")
        self.contact_label.setProperty('class', 'cal-label')
        self.contact_label.setFixedHeight(62)
        self.hbox_2.addWidget(self.contact_label)
        
        # Divide the screen into halves
        self.vbox_1 = QVBoxLayout()
        self.vbox_2 = QVBoxLayout()
        
        self.contact_desc_1 = QLabel("Our Leadership")
        self.contact_desc_1.setProperty('class', 'bold-under-label')
        self.contact_desc_1.setWordWrap(True)
        self.vbox_1.addWidget(self.contact_desc_1)
        
        self.contact_desc_2 = QLabel("President: Donald D. Shlump\nE-Mail: royalschlumpness@gmail.com\n" + \
                                     "Phone Number: (608)-555-6969\n")
        self.contact_desc_2.setProperty('class', 'acc-desc-label')
        self.contact_desc_2.setWordWrap(True)
        self.hbox_4.addWidget(self.contact_desc_2)
        self.contact_desc_7 = QLabel("Executive Director: Barracks Slowbama\nE-Mail: doodoowater@gmail.com\n" + \
                                     "Phone Number: (608)-555-1234\n")
        self.contact_desc_7.setProperty('class', 'acc-desc-label')
        self.contact_desc_7.setWordWrap(True)
        self.hbox_4.addWidget(self.contact_desc_7)
        self.vbox_1.addLayout(self.hbox_4)
        
        self.contact_desc_3 = QLabel("Other Contacts")
        self.contact_desc_3.setProperty('class', 'bold-under-label')
        self.vbox_1.addWidget(self.contact_desc_3)
        
        self.contact_desc_4 = QLabel("Staffing Manager: Darth Fader\nE-Mail: deathstar@gmail.com\n" + \
                                     "Phone Number: (608)-555-6666\n")
        self.contact_desc_4.setProperty('class', 'acc-desc-label')
        self.contact_desc_4.setWordWrap(True)
        self.hbox_5.addWidget(self.contact_desc_4)
        self.contact_desc_8 = QLabel("Volunteering Manager: Ray-Ray McBeans\nE-Mail: bakethembeans@gmail.com\n" + \
                                     "Phone Number: (608)-555-0911\n")
        self.contact_desc_8.setProperty('class', 'acc-desc-label')
        self.contact_desc_8.setWordWrap(True)
        self.hbox_5.addWidget(self.contact_desc_8)
        self.vbox_1.addLayout(self.hbox_5)
        
        self.contact_desc_5 = QLabel("Helping Hands Headquarters")
        self.contact_desc_5.setProperty('class', 'bold-under-label')
        self.vbox_1.addWidget(self.contact_desc_5)
        
        self.contact_desc_6 = QLabel("Helping Hands Headquarters\n2851 Bell Island Dr, La Crosse, WI 54603\n" + \
                                     "Phone Number: (608)-555-4444")
        self.contact_desc_6.setProperty('class', 'acc-desc-label')
        self.contact_desc_6.setWordWrap(True)
        self.vbox_1.addWidget(self.contact_desc_6)
        
        # create labels for the information
        self.image_title = QLabel("Come Visit Us!")
        self.image_title.setProperty('class', 'home-events-label')
        self.image_title.setFixedHeight(40)
        self.image_title.setAlignment(Qt.AlignCenter)
        self.vbox_2.addWidget(self.image_title)
        
        # retrieve system resolution
        sys_width, sys_height = self.screen_resolution()
        
        # set up the image
        self.about_image = QLabel(self)
        
        # if file exists else use the other one (handles path to the image)
        if os.path.isfile('gui\\photos\\contact.png'):
            pixmap = QPixmap('gui\\photos\\contact.png')
        else:
            pixmap = QPixmap('non_profit\\gui\\photos\\contact.png')
        
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
        self.spacer_2.setProperty('class', 'contact-bottom-spacer-label')
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
