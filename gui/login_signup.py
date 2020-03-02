'''
Manages the relationship between all of the different pages.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

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
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        # set up the login button
        login = QPushButton("Login")
        login.clicked.connect(self.login_click)
        login.setProperty('class', 'login-btn')
        login.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the sign up button
        signup = QPushButton("Sign-Up")
        signup.clicked.connect(self.signup_click)
        signup.setProperty('class', 'signup-btn')
        signup.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the guest button
        guest = QPushButton("Continue as Guest")
        guest.clicked.connect(self.guest_click)
        guest.setProperty('class', 'signup-btn')
        guest.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(login)
        vbox.addWidget(signup)
        vbox.addWidget(guest)
        vbox.addStretch(1)
        
        # set up the layout
        self.setLayout(vbox)
        
        # set the geometry of the window
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = sys_width / 2 - 250
        self.y_coord = sys_height / 4
        self.width = 500
        self.height = 500
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # resets the coordinates of the window after switching to this page
    def set_position(self):
        self.parent().move(self.x_coord, self.y_coord)
        self.parent().resize(self.width, self.height)
    
    # go to the login page
    def login_click(self):
        self.win.set_page(1)
    
    # go to the new account page
    def signup_click(self):
        self.win.set_page(2)
    
    # go to the homepage
    def guest_click(self):
        self.win.set_page(4)
    
    # draws rectangle around buttons
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(1, 135, 498, 225)
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)
        
        return geometry.width(), geometry.height()
