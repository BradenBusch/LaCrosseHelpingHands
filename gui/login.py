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
        self.username_check = QLineEdit()
        self.password_check = QLineEdit()

        self.draw()

    def draw(self):
        label = QLabel("BPW")

        # label.setAlignment(Qt.AlignCenter)

    # Check database, verify the username and password.
    def verify_fields(self, entered_username, entered_password):
        try:
            username_check = User.get(User.username == entered_username)
        except User.DoesNotExist:
            username_check = None
        if username_check is None:
            # TODO how we want to handle login/failed login
            return
        hashed_password = User.get(User.username == username_check)
        if self.verify_fields(hashed_password, entered_password) is not True:
            return
        else:
            return

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
