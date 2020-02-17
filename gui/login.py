from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import hashlib
import binascii


class Login(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QLabel("BPW")
        # label.setAlignment(Qt.AlignCenter)

    # Check database, verify the username and password.
    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
