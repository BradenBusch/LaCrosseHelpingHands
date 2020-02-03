from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from non_profit.gui.new_account import NewAccount
from non_profit.gui.login import Login


# Builds the "Username / Password" portion of the GUI (the login screen)
class LogInSignUp(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("login_signup")
        self.draw()
        self.show()
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    # These methods will update the database and perform checks
    def login_click(self):
        pass

    def draw(self):
        # style this, she dumb ugly doe
        login = QPushButton("Login")
        login.clicked.connect(self.login_click)
        signup = QPushButton("Sign-Up")
        signup.clicked.connect(self.signup_click)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(login)
        vbox.addWidget(signup)
        self.setGeometry(0, 0, 300, 300)
        self.setLayout(vbox)

    # These methods will update the database and perform checks
    def signup_click(self):
        NewAccount()
        self.close()

    def login_click(self):
        Login()
        self.close()
