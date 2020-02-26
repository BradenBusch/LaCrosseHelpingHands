from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDesktopWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from non_profit.gui.calendar import Calendar
    from non_profit.gui.new_account import NewAccount
    from non_profit.gui.login import Login
    from non_profit.gui.login_signup import LogInSignUp
except:
    from gui.calendar import Calendar
    from gui.new_account import NewAccount
    from gui.login import Login
    from gui.login_signup import LogInSignUp


class LogInSignUp2(QWidget):

    switch_window = pyqtSignal()
    switch_window2 = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty('class', 'login-signup')
        self.draw()
        self.setWindowTitle("Helping Hands La Crosse")
        self.update()

    def draw(self):
        login = QPushButton("Login")
        login.clicked.connect(self.login_click)
        login.setProperty('class', 'login-btn')
        login.setCursor(QCursor(Qt.PointingHandCursor))

        signup = QPushButton("Sign-Up")
        signup.clicked.connect(self.signup_click)
        signup.setProperty('class', 'signup-btn')
        signup.setCursor(QCursor(Qt.PointingHandCursor))

        guest = QPushButton("Continue as Guest")
        guest.clicked.connect(self.guest_click)
        guest.setProperty('class', 'signup-btn')
        guest.setCursor(QCursor(Qt.PointingHandCursor))

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(login)
        vbox.addWidget(signup)
        vbox.addWidget(guest)
        # self.setGeometry(0, 0, 300, 300)
        self.setLayout(vbox)

    def login_click(self):
        self.switch_window.emit()

    def signup_click(self):
        self.switch_window2.emit()


class Controller:

    def __init__(self):
        pass

    def show_login_signup(self):
        login_signup = LogInSignUp2()
        login_signup.switch_window.connect(self.show_login)
        login_signup.switch_window2.connect(self.show_signup)
        login_signup.show()

    def show_login(self):
        pass
        #login = Login2()

