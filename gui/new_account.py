'''
New Account page of the application, where users will register their new account
with the organization.

Accessibile by: Guest

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/21/2020

'''

import os
import hashlib
import binascii

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
        self.win = None
        
        # set the page id
        self.this_page = cs.PAGE_NEW_ACCOUNT
        
        # set up all fields to be filled in by the user
        self.username_edit = QLineEdit()
        self.username_edit.setMaxLength(30)
        self.email_edit = QLineEdit()
        self.email_edit.setMaxLength(30)
        self.password_edit = QLineEdit()
        self.password_edit.setMaxLength(30)
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setMaxLength(30)
        self.staff_code_box = QLineEdit()
        self.staff_code_box.setMaxLength(30)
        self.staff_code_box.hide()
        self.admin_code_box = QLineEdit()
        self.admin_code_box.setMaxLength(30)
        self.admin_code_box.hide()
        self.radio_btns = []
        self.fields = [self.username_edit,
                       self.email_edit,
                       self.password_edit,
                       self.confirm_password_edit,
                       self.staff_code_box,
                       self.admin_code_box]
        
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
        
        # set up the volunteer radio button
        self.volunteer_radio = QRadioButton("Volunteer")
        self.volunteer_radio.toggled.connect(self.hide_staff)
        self.volunteer_radio.toggled.connect(self.hide_admin)
        self.volunteer_radio.setChecked(True)
        
        # set up the staff radio button
        self.staff_radio = QRadioButton("Staff")
        self.staff_radio.toggled.connect(self.hide_admin)
        self.staff_radio.toggled.connect(self.staff_click)
        
        # set up the administrator radio button
        self.admin_radio = QRadioButton("Administrator")
        self.admin_radio.toggled.connect(self.hide_staff)
        self.admin_radio.toggled.connect(self.admin_click)
        
        # set up the radio buttons
        self.radio_btns.append(self.volunteer_radio)
        self.radio_btns.append(self.staff_radio)
        self.radio_btns.append(self.admin_radio)
        
        # set up the text fields to be filled in by the user
        self.username_edit.setPlaceholderText("Username (At least 8 characters)")
        self.email_edit.setPlaceholderText("E-Mail")
        self.password_edit.setPlaceholderText("Password (At least 8 characters)")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        # self.confirm_password_edit.returnPressed.connect(self.verify_fields)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.staff_code_box.setPlaceholderText("Enter the Staff Code")
        self.staff_code_box.setEchoMode(QLineEdit.Password)
        self.admin_code_box.setPlaceholderText("Enter the Administrator Code")
        self.admin_code_box.setEchoMode(QLineEdit.Password)
        
        # set up the VBox
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.username_edit)
        self.vbox.addWidget(self.email_edit)
        self.vbox.addWidget(self.password_edit)
        self.vbox.addWidget(self.confirm_password_edit)
        self.vbox.addWidget(self.staff_code_box)
        self.vbox.addWidget(self.admin_code_box)
        
        # set up the HBox
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        
        for btn in self.radio_btns:
            self.hbox_1.addWidget(btn)
        
        self.hbox_2.addWidget(self.cancel_btn)
        self.hbox_2.addWidget(self.confirm_btn)
        
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
        # retrieve the information the user entered
        password = self.password_edit.text()
        confirm_pass = self.confirm_password_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        
        # attempt to retrieve the user from the database
        try:
            username_check = User.get(User.username == username)
        except User.DoesNotExist:
            username_check = None
        try:
            email_check = User.get(User.account_email == email)
        except User.DoesNotExist:
            email_check = None

        # ensure the user entered viable information
        if len(username) < 8:
            msg = QMessageBox.warning(self, " ", " Your Username must be 8 characters or longer. ")
            self.username_edit.clear()
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        # email must not be an empty string
        elif len(email) == 0:
            msg = QMessageBox.warning(self, " ", " You must enter an E-Mail address. ")
            self.email_edit.clear()
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        # password must be 8 characters
        elif len(password) < 8:
            msg = QMessageBox.warning(self, " ", " Your Password must be 8 characters or longer. ")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        # passwords must match
        elif password != confirm_pass:
            msg = QMessageBox.warning(self, " ", " Your Passwords do not match. ")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        # username is already taken
        elif username_check is not None:
            msg = QMessageBox.warning(self, " ", " That Username is already taken. Try another. ")
            self.username_edit.clear()
            return
        # email is already taken
        elif email_check is not None:
            msg = QMessageBox.warning(self, " ", " That E-Mail is already taken. Log in or use a different E-Mail. ")
            self.email_edit.clear()
            return
        # staff code wasn't entered properly
        elif self.get_account_type() == "Staff" and self.staff_code_box.text() != cs.STAFF_CODE:
            msg = QMessageBox.warning(self, " ", " You entered the wrong Staff Code. ")
            self.staff_code_box.clear()
            return
        # admin code wasn't entered properly
        elif self.get_account_type() == "Administrator" and self.admin_code_box.text() != cs.ADMIN_CODE:
            msg = QMessageBox.warning(self, " ", " You entered the wrong Administrator Code. ")
            self.admin_code_box.clear()
            return
        # return to the login page, all checks passed
        else:
            QMessageBox.about(self, " ", " Account creation successful!")
            stored_password = hash_password(password)
            account_type = self.get_account_type()
            self.store_user(username, email, stored_password, account_type)
            self.go_back_success()
            return
    
    # clears all fields in the forum
    def clear_fields(self):
        for f in self.fields:
            f.clear()
    
    # store the new user's information in the database
    def store_user(self, username, email, password, account_type=None):
        new_user = User(username=username, password=password, account_email=email, account_type=account_type, event_ids='-1', volunteer_hours=0.0, total_donations=0)
        new_user.save()
    
    # go back to the previous page
    def go_back(self):
        self.win.set_page(self.this_page, cs.PREV_PAGE)
        self.clear_fields()
    
    # go back to the login screen if account creation was successful
    def go_back_success(self):
        self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
        self.clear_fields()
    
    # show the staff_code text box widget
    def staff_click(self):
        self.staff_code_box.show()

    # hide the staff_code text box widget
    def hide_staff(self):
        self.staff_code_box.hide()
        self.staff_code_box.clear()
    
    # show the admin_code text box widget
    def admin_click(self):
        self.admin_code_box.show()
    
    # hide the admin_code text box widget
    def hide_admin(self):
        self.admin_code_box.hide()
        self.admin_code_box.clear()
    
    # get which radio button is selected
    def get_account_type(self):
        for btn in self.radio_btns:
            if btn.isChecked():
                return btn.text()
    
    # draws rectangle around buttons
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(1, 1, 498, 490)
    
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


# hash the user's password
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
