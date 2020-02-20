from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

try:
    from non_profit.gui.login_signup import *
    from non_profit.models.database import *
except:
    from gui.login_signup import *
    from models.database import *

import random, hashlib, binascii, os


# Class that handles the 'Sign-Up' screen.
class NewAccount(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()
        self.admin_code_box = QLineEdit()
        self.admin_code_box.hide()
        self.fields = [self.username_edit, self.email_edit, self.password_edit, self.confirm_password_edit]
        self.radio_btns = []
        self.vbox = QVBoxLayout()
        self.draw()

    # Build Create Account window
    def draw(self):
        # self.setFixedSize(300, 300)
        self.setWindowTitle("Make a new account")

        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        confirm_btn = QPushButton()
        cancel_btn = QPushButton()
        confirm_btn.clicked.connect(self.verify_fields)
        cancel_btn.clicked.connect(self.go_back)

        volunteer_radio = QRadioButton('Volunteer')
        volunteer_radio.setChecked(True)
        volunteer_radio.toggled.connect(self.hide_admin)
        staff_radio = QRadioButton('Staff')
        staff_radio.toggled.connect(self.hide_admin)
        admin_radio = QRadioButton('Admin')
        admin_radio.toggled.connect(self.admin_click)
        self.radio_btns.append(volunteer_radio)
        self.radio_btns.append(staff_radio)
        self.radio_btns.append(admin_radio)
        confirm_btn.setText("Confirm")
        cancel_btn.setText("Cancel")
        self.username_edit.setPlaceholderText("Username (At least 8 Characters)")
        self.email_edit.setPlaceholderText("E-Mail")  # If we aren't going to do password recovery we can delete this
        self.password_edit.setPlaceholderText("Password (At least 8 Characters)")
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.returnPressed.connect(self.verify_fields)
        self.admin_code_box.setPlaceholderText("Enter the Admin Password")

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.vbox.addWidget(self.username_edit)
        self.vbox.addWidget(self.email_edit)
        self.vbox.addWidget(self.password_edit)
        self.vbox.addWidget(self.confirm_password_edit)
        self.vbox.addWidget(self.admin_code_box)

        for btn in self.radio_btns:
            hbox1.addWidget(btn)

        hbox2.addWidget(cancel_btn)
        hbox2.addWidget(confirm_btn)
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.setLayout(self.vbox)

    # Show the admin code widget
    def admin_click(self):
        self.admin_code_box.show()

    # Hide the admin code widget.
    def hide_admin(self):
        self.admin_code_box.hide()

    # Verifies that the Username/Email aren't in use, that the passwords match, and the passwords are 8 characters long
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
        # Move to the next GUI, all checks passed
        else:
            msg = QMessageBox.warning(None, " ", "Beep")
            user_id = self.generate_id()
            stored_password = hash_password(password)
            account_type = self.get_account_type()
            self.store_user(user_id, username, email, stored_password, account_type)
            self.go_back()
            return

    # Clear all fields in the forum.
    def clear_fields(self):
        for f in self.fields:
            f.clear()

    # Go back to the Login / Signup page
    def go_back(self):
        self.close()
        self.parent().parent().set_page(0)

    # Get which radio button is selected
    def get_account_type(self):
        for btn in self.radio_btns:
            if btn.isChecked():
                return btn.text()

    # Store the new users information in the database
    def store_user(self, user_id, username, email, password, account_type=None):
        new_user = User(account_id=user_id, username=username, password=password, account_email=email, account_type=account_type)
        new_user.save()
        query = User.select()
        print([user.username for user in query])

    # TODO check id's, if this is even needed anyway
    # Generate a unique ID for each user in the database
    def generate_id(self):
        # return uuid.uuid4().hex[:4]
        digits = set(range(10))
        first = random.randint(1, 9)
        last_3 = random.sample(digits - {first}, 3)
        return str(first) + ''.join(map(str, last_3))


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


# returns the resolution of the current system (width and height)
def screen_resolution():
    sizeObject = QDesktopWidget().screenGeometry(0)
    return sizeObject.width(), sizeObject.height()
