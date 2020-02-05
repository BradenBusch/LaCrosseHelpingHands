from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from non_profit.gui.login_signup import *
import random


class NewAccount(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()
        self.fields = [self.username_edit, self.email_edit, self.password_edit, self.confirm_password_edit]
        self.draw()

    # Build Create Account window
    def draw(self):
        self.setFixedSize(300, 200)
        self.setWindowTitle("Make a new account")

        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        confirm_btn = QPushButton()
        cancel_btn = QPushButton()
        confirm_btn.clicked.connect(self.verify_fields)
        cancel_btn.clicked.connect(lambda: self.close())

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
        hbox.addWidget(cancel_btn)
        hbox.addWidget(confirm_btn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    # Verifies that the Username/Email aren't in use, that the passwords match, and the passwords are 8 characters long
    def verify_fields(self):
        password = self.password_edit.text()
        confirm_pass = self.confirm_password_edit.text()
        username = self.username_edit.text()
        email = self.username_edit.text()

        if len(email) == 0:
            msg = QMessageBox.warning(None, " ", "Enter an email address!")
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
            msg = QMessageBox.warning(None, " ", "Your passwords don't match!")
            self.clear_fields()
            return
        # TODO check database for username and email
        else:
            pass  # move to next GUI (homepage)

    def clear_fields(self):
        for f in self.fields:
            f.clear()

    # Store the new users information in the database
    def store_user(self):
        user_id = self.generate_id()

    # Generate a unique ID for each user in the database
    def generate_id(self):
        # return uuid.uuid4().hex[:4]
        digits = set(range(10))
        first = random.randint(1, 9)
        last_3 = random.sample(digits - {first}, 3)
        return str(first) + ''.join(map(str, last_3))
