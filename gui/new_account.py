from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from non_profit.gui.login_signup import *
from non_profit.models.database import *

import random, hashlib, binascii, os


class NewAccount(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()
        self.fields = [self.username_edit, self.email_edit, self.password_edit, self.confirm_password_edit]
        self.radio_btn_names = ['Volunteer', 'Staff', 'Admin']

        self.draw()

    # Build Create Account window
    # TODO add checkboxes for choosing an account type (admin needs extra code or something idk)
    def draw(self):
        self.setFixedSize(300, 300)
        self.setWindowTitle("Make a new account")

        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        confirm_btn = QPushButton()
        cancel_btn = QPushButton()
        confirm_btn.clicked.connect(self.verify_fields)
        cancel_btn.clicked.connect(self.go_back)  # TODO nah we gotta go back

        volunteer_radio = QRadioButton('Volunteer')
        volunteer_radio.setChecked(True)
        staff_radio = QRadioButton('Staff')
        admin_radio = QRadioButton('Admin')

        confirm_btn.setText("Confirm")
        cancel_btn.setText("Cancel")
        self.username_edit.setPlaceholderText("Username (At least 8 Characters)")
        self.email_edit.setPlaceholderText("E-Mail")  # If we aren't going to do password recovery we can delete this
        self.password_edit.setPlaceholderText("Password (At least 8 Characters)")
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.returnPressed.connect(self.verify_fields)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.username_edit)
        vbox.addWidget(self.email_edit)
        vbox.addWidget(self.password_edit)
        vbox.addWidget(self.confirm_password_edit)
        vbox.addWidget(volunteer_radio)
        vbox.addWidget(staff_radio)
        vbox.addWidget(admin_radio)
        hbox.addWidget(cancel_btn)
        hbox.addWidget(confirm_btn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    # Verifies that the Username/Email aren't in use, that the passwords match, and the passwords are 8 characters long
    def verify_fields(self):
        password = self.password_edit.text()
        confirm_pass = self.confirm_password_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        username_check = User.select().where(User.user_name == username)
        email_check = User.select().where(User.account_email == email)
        if len(email) == 0:
            msg = QMessageBox.warning(None, " ", "You must enter an email address.")
            self.clear_fields()
            return
        elif len(username) < 8:
            msg = QMessageBox.warning(None, " ", "Your Username must be 8 characters or longer.")
            self.clear_fields()
            return
        elif len(password) < 8:
            msg = QMessageBox.warning(None, " ", "Your Password must be 8 characters or longer.")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        elif password != confirm_pass:
            msg = QMessageBox.warning(None, " ", "Your passwords don't match.")
            self.clear_fields()
            return
        # TODO check database for username and email
        elif username_check.exists():
            pass  # Username taken, handle
        elif email_check.exists():
            pass  # Email taken
        # Move to the next GUI, all checks passed
        else:
            stored_password = hash_password(password)
            self.store_user(username, email, stored_password)  # TODO account type

    def clear_fields(self):
        for f in self.fields:
            f.clear()

    def go_back(self):
        self.close()
        self.parent().parent().set_page(0)
        pass

    # Store the new users information in the database
    # TODO make passwords encrypted
    def store_user(self, username, email, password, account_type=None):
        user_id = self.generate_id()
        hashed_pass = hash_password(password)
        new_user = User(user_id=user_id, username=username, password=hashed_pass, email=email, account_type=account_type)
        new_user.save()

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
