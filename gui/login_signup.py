'''
Holds everything related to the welcome page, where users decide how to access the application.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit.gui.new_account import NewAccount
    from non_profit.gui.login import Login
    from non_profit import constants as cs
except:
    from gui.new_account import NewAccount
    from gui.login import Login
    import constants as cs


class LogInSignUp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'login-signup')
        self.setWindowTitle("Helping Hands La Crosse")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_LOGIN_SIGNUP
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        # set up the login button
        self.login_btn = QPushButton("Log In")
        self.login_btn.clicked.connect(self.login_click)
        self.login_btn.setProperty('class', 'login-btn')
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the sign up button
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.signup_click)
        self.signup_btn.setProperty('class', 'signup-btn')
        self.signup_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the guest button
        self.guest_btn = QPushButton("Continue as Guest")
        self.guest_btn.clicked.connect(self.guest_click)
        self.guest_btn.setProperty('class', 'signup-btn')
        self.guest_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the VBox
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.login_btn)
        self.vbox.addWidget(self.signup_btn)
        self.vbox.addWidget(self.guest_btn)
        self.vbox.addStretch(1)
        self.vbox.setAlignment(Qt.AlignCenter)
        
        # set up the layout
        self.setLayout(self.vbox)
        
        # set the geometry of the window
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = sys_width / 2 - 250
        self.y_coord = sys_height / 4
        self.width = 500
        self.height = 500
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # go to the login page
    def login_click(self):
        self.win.set_page(self.this_page, cs.PAGE_LOGIN)
    
    # go to the new account page
    def signup_click(self):
        self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
    
    # go to the homepage
    def guest_click(self):
        self.win.set_page(self.this_page, cs.PAGE_CAL)    # TODO change cs.PAGE_CAL to cs.PAGE_HOME when homepage is done
    
    # draws rectangle around buttons
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(1, 135, 498, 225)
    
    # resets the coordinates of the window after switching to this page
    def set_position(self):
        self.parent().move(self.x_coord, self.y_coord)
        self.parent().resize(self.width, self.height)
    
    # checks which user is logged in and formats the page to accomodate the user type
    def check_user(self):
        # check if the current user is a guest
        if cs.CURRENT_USER == "Guest":
            pass
        
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
