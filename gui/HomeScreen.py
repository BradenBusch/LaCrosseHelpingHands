from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QLabel
from functools import partial
from non_profit.gui.NewAccount import NewAccount

# Builds the "Username / Password" portion of the GUI (the login screen)
class HomeScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("homescreen")
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
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(login)
        vbox.addWidget(signup)
        self.setGeometry(0, 0, 300, 300)
        self.setLayout(vbox)


def signup_click():
    NewAccount()
