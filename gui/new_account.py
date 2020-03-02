'''
Holds everything related to the login page.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

import os
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


class NewAccount(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # set window title and initialize the window reference
        self.setWindowTitle("Create an Account")
        
        # set up all fields to be filled in by the user
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()
        self.admin_code_box = QLineEdit()
        self.admin_code_box.hide()
        self.fields = [self.username_edit, self.email_edit, self.password_edit, self.confirm_password_edit]
        self.radio_btns = []
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        #
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.admin_code_box.setEchoMode(QLineEdit.Password)
        
        # set up the confirm button
        confirm_btn = QPushButton("Confirm")
        confirm_btn.clicked.connect(self.verify_fields)
        confirm_btn.setProperty('class', 'confirm-btn')
        confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.go_back)
        cancel_btn.setProperty('class', 'cancel-btn')
        cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # set up the volunteer radio button
        volunteer_radio = QRadioButton("Volunteer")
        volunteer_radio.toggled.connect(self.hide_admin)
        volunteer_radio.setChecked(True)
        
        # set up the staff radio button
        staff_radio = QRadioButton("Staff")
        staff_radio.toggled.connect(self.hide_admin)
        
        # set up the administrator radio button
        admin_radio = QRadioButton("Administrator")
        admin_radio.toggled.connect(self.admin_click)
        
        # set up the radio buttons
        self.radio_btns.append(volunteer_radio)
        self.radio_btns.append(staff_radio)
        self.radio_btns.append(admin_radio)
        
        # set up the text fields to be filled in by the user
        self.username_edit.setPlaceholderText("Username (At least 8 Characters)")
        self.email_edit.setPlaceholderText("E-Mail")  # If we aren't going to do password recovery we can delete this
        self.password_edit.setPlaceholderText("Password (At least 8 Characters)")
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.returnPressed.connect(self.verify_fields)
        self.admin_code_box.setPlaceholderText("Enter the Admin Password")
        
        # set up the VBox
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.username_edit)
        self.vbox.addWidget(self.email_edit)
        self.vbox.addWidget(self.password_edit)
        self.vbox.addWidget(self.confirm_password_edit)
        self.vbox.addWidget(self.admin_code_box)
        
        # set up the HBox
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        
        for btn in self.radio_btns:
            self.hbox_1.addWidget(btn)
        
        self.hbox_2.addWidget(cancel_btn)
        self.hbox_2.addWidget(confirm_btn)
        
        # add the HBoxes to the VBox
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        
        # set up the layout
        self.setLayout(self.vbox)
        
        # set the geometry of the window
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = sys_width / 2 - 250
        self.y_coord = sys_height / 4
        self.width = 500
        self.height = 500
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # verify that the Username/Email aren't in use, that the passwords match, and the passwords are 8 characters long
    def verify_fields(self):
        password = self.password_edit.text()
        confirm_pass = self.confirm_password_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        
        try:
            username_check = User.get(User.username == username)
        except User.DoesNotExist:
            username_check = None
        try:
            email_check = User.get(User.account_email == email)
        except User.DoesNotExist:
            email_check = None

        # ensure the user entered viable information
        if len(email) == 0:
            msg = QMessageBox.warning(None, " ", " You must enter an email address. ")
            self.clear_fields()
            return
        
        elif len(username) < 8:
            msg = QMessageBox.warning(None, " ", " Your Username must be 8 characters or longer. ")
            self.clear_fields()
            return
        
        elif len(password) < 8:
            msg = QMessageBox.warning(None, " ", " Your Password must be 8 characters or longer. ")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        
        elif password != confirm_pass:
            msg = QMessageBox.warning(None, " ", " Your passwords don't match. ")
            self.clear_fields()
            return
        
        elif username_check is not None:
            msg = QMessageBox.warning(None, " ", " That username is already taken. Try another. ")
            self.username_edit.clear()
            return
        
        elif email_check is not None:
            msg = QMessageBox.warning(None, " ", " That email is already taken. Sign-in or use a different email. ")
            self.email_edit.clear()
            return
        
        elif self.get_account_type() == 'Admin' and self.admin_code_box.text() != cs.ADMIN_PASSWORD:
            msg = QMessageBox.warning(None, " ", " You entered the wrong admin password. ")
            self.admin_code_box.clear()
            return
        
        # return to the login page, all checks passed
        else:
            msg = QMessageBox.warning(None, " ", " Account created successfully. ")
            stored_password = hash_password(password)
            account_type = self.get_account_type()
            self.store_user(username, email, stored_password, account_type)
            self.go_back()
            return
    
    # clears all fields in the forum
    def clear_fields(self):
        for f in self.fields:
            f.clear()
    
    # store the new user's information in the database
    def store_user(self, username, email, password, account_type=None):
        new_user = User(username=username, password=password, account_email=email, account_type=account_type)
        new_user.save()
        query = User.select()
        print([user.user_id for user in query])
    
    # hash the user's password
    def hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    # resets the coordinates of the window after switching to this page
    def set_position(self):
        self.parent().move(self.x_coord, self.y_coord)
        self.parent().resize(self.width, self.height)
    
    # go back to the login page
    def go_back(self):
        self.win.set_page(0)
    
    # show the admin code widget
    def admin_click(self):
        self.admin_code_box.show()
    
    # hide the admin code widget.
    def hide_admin(self):
        self.admin_code_box.hide()
    
    # get which radio button is selected
    def get_account_type(self):
        for btn in self.radio_btns:
            if btn.isChecked():
                return btn.text()
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)
        
        return geometry.width(), geometry.height()
