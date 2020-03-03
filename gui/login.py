'''
Holds everything related to the login page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

import hashlib
import binascii

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit.gui.login_signup import *
    from non_profit.models.database import *
    from non_profit import constants as cs
except:
    from gui.login_signup import *
    from models.database import *
    import constants as cs


class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and initialize the window reference
        self.setWindowTitle("Log In")
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_LOGIN
        
        # set up the username label
        self.username_label = QLabel("Username")
        self.username_label.setProperty('class', 'login-label')
        
        # set up the username check
        self.username_check = QLineEdit()
        
        # set up the password label
        self.password_label = QLabel("Password ")
        self.password_label.setProperty('class', 'login-label')
        
        # set up the password check
        self.password_check = QLineEdit()
        self.password_check.setEchoMode(QLineEdit.Password)
        
        # set up fields
        self.fields = [self.username_check, self.password_check]
        
        # set up the HBox and VBox to be used by the layout
        self.vbox = QVBoxLayout()
        self.user_hbox = QHBoxLayout()
        self.pass_hbox = QHBoxLayout()
        self.confirm_hbox = QHBoxLayout()
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        # set up the confirm button
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self.verify_fields)
        self.confirm_btn.setProperty('class', 'confirm-btn')
        self.confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.go_back)
        self.cancel_btn.setProperty('class', 'cancel-btn')
        self.cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the HBox
        self.user_hbox.addWidget(self.username_label)
        self.user_hbox.addWidget(self.username_check)
        self.pass_hbox.addWidget(self.password_label)
        self.pass_hbox.addWidget(self.password_check)
        self.confirm_hbox.addWidget(self.cancel_btn)
        self.confirm_hbox.addWidget(self.confirm_btn)
        
        # set up the VBox
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.user_hbox)
        self.vbox.addLayout(self.pass_hbox)
        self.vbox.addLayout(self.confirm_hbox)
        self.vbox.addStretch(1)
        
        # set up the layout
        self.setLayout(self.vbox)
        
        # set the geometry of the window
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = sys_width / 2 - 250
        self.y_coord = sys_height / 4
        self.width = 500
        self.height = 500
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # check the database, verify the username and password of the user
    def verify_fields(self):
        entered_username = self.username_check.text()
        entered_password = self.password_check.text()
        
        # attempt to retrieve the user's information from the database
        try:
            username_check = User.get(User.username == entered_username).username
        except User.DoesNotExist:
            username_check = None
        
        # retrieve and check the password
        hashed_password = User.get(User.username == username_check).password  # Get the protected password from db
        password_check = self.verify_password(hashed_password, entered_password)  # True if passwords match, else false
        
        # ensure the user entered viable information
        if len(entered_username) < 8 or len(entered_password) < 8:
            msg = QMessageBox.warning(None, " ", " Enter a username and password of valid length (greater than 8)")
            self.username_check.clear()
            self.password_check.clear()
            return
        
        elif username_check is None:
            msg = QMessageBox.warning(None, " ", " That username doesn't exist. Try another. ")
            self.username_check.clear()
            self.password_check.clear()
            return
        
        elif password_check is not True:
            msg = QMessageBox.warning(None, " ", " Incorrect Password. Try re-entering. ")
            self.password_check.clear()
            return
        else:
            cs.CURRENT_USER = User.get(User.username == entered_username).account_type
            print(cs.CURRENT_USER)
            self.go_forward()
            return
    
    # verify that the password entered for the user is the correct password
    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        
        return pwdhash == stored_password
    
    # go back to the previous page
    def go_back(self):
        self.win.set_page(self.this_page, cs.PREV_PAGE)
        self.username_check.clear()
        self.password_check.clear()
    
    # go to the homepage
    def go_forward(self):
        # go back to the original page after logging in
        if cs.PREV_PAGE is not cs.PAGE_LOGIN_SIGNUP:
            self.win.set_page(self.this_page, cs.PREV_PAGE)
        
        # go to the homepage if the user is coming from the login signup page
        else:
            self.win.set_page(self.this_page, cs.PAGE_CAL)  # TODO change cs.PAGE_CAL to cs.PAGE_HOME when homepage is done
        
        self.username_check.clear()
        self.password_check.clear()
    
    # draws rectangle around buttons
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(1, 160, 498, 175)
    
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
