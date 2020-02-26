from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

try:
    from non_profit.gui.login_signup import *
    from non_profit.models.database import *
except:
    from gui.login_signup import *
    from models.database import *

import hashlib
import binascii


class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_label = QLabel('Username')
        self.username_check = QLineEdit()
        self.password_label = QLabel('Password ')
        self.password_check = QLineEdit()
        self.fields = [self.username_check, self.password_check]
        self.vbox = QVBoxLayout()
        self.user_hbox = QHBoxLayout()
        self.pass_hbox = QHBoxLayout()
        self.confirm_hbox = QHBoxLayout()
        self.draw()

    def draw(self):
        self.setWindowTitle("Login")
        confirm_btn = QPushButton()
        confirm_btn.setProperty('class', 'confirm-btn')
        confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        confirm_btn.setText("Confirm")
        confirm_btn.clicked.connect(self.verify_fields)
        cancel_btn = QPushButton()
        cancel_btn.setProperty('class', 'cancel-btn')
        cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_btn.setText("Cancel")
        cancel_btn.clicked.connect(self.go_back)

        self.password_check.setEchoMode(QLineEdit.Password)
        self.username_label.setProperty('class', 'login-label')
        self.password_label.setProperty('class', 'login-label')

        self.vbox.addStretch(1)
        self.user_hbox.addWidget(self.username_label)
        self.user_hbox.addWidget(self.username_check)
        self.pass_hbox.addWidget(self.password_label)
        self.pass_hbox.addWidget(self.password_check)
        self.confirm_hbox.addWidget(cancel_btn)
        self.confirm_hbox.addWidget(confirm_btn)
        self.vbox.addLayout(self.user_hbox)
        self.vbox.addLayout(self.pass_hbox)
        self.vbox.addLayout(self.confirm_hbox)
        self.setLayout(self.vbox)
        # label.setAlignment(Qt.AlignCenter)

    # Check database, verify the username and password.
    def verify_fields(self):
        entered_username = self.username_check.text()
        entered_password = self.password_check.text()
        try:
            username_check = User.get(User.username == entered_username).username
        except User.DoesNotExist:
            username_check = None
        hashed_password = User.get(User.username == username_check).password  # Get the protected password from db
        password_check = self.verify_password(hashed_password, entered_password)  # True if passwords match, else false

        if len(entered_username) < 8 or len(entered_password) < 8:
            msg = QMessageBox.warning(None, " ", " Enter a username and password of valid length (greater than 8)")
            return
        elif username_check is None:
            msg = QMessageBox.warning(None, " ", " That username doesn't exist. Try another. ")
            return
        elif password_check is not True:
            msg = QMessageBox.warning(None, " ", " Incorrect Password. Try re-entering. ")
            return
        else:
            msg = QMessageBox.warning(None, " ", "BEEP!")
            return

    def go_back(self):
        self.close()
        self.parent().parent().set_page(0)

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
