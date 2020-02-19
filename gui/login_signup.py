from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDesktopWidget, QLabel

try:
    from non_profit.gui.new_account import NewAccount
    from non_profit.gui.login import Login
except:
    from gui.new_account import NewAccount
    from gui.login import Login


# The Stack GUI. This allows multiple windows to be opened from buttons.
class LoginNewAccountStacker(QWidget):
    def __init__(self, widgets, main=None):
        super().__init__()
        self.widgets = widgets
        self.stacker = QStackedWidget(self)
        self.win = main
        for widget in self.widgets:
            self.stacker.addWidget(widget)
        # I have no idea why this works, but don't touch it.
        # --------------------------------------------------
        self.v = QVBoxLayout()
        self.v.addWidget(QWidget())
        self.v.addWidget(self.stacker)
        self.setLayout(self.v)
        # --------------------------------------------------
        self.set_page(0)
        width, height = screen_resolution()
        self.setGeometry(width/2 - 250, height/2 - 250, 500, 500)

    # Not sure if this is necessary yet
    def windowTitle(self):
        return self.widgets[self.stacker.currentIndex()].windowTitle()

    # TODO fix window naming so that it updates
    def set_page(self, i):
        if not i < len(self.widgets):
            return
        self.win.setWindowTitle(self.widgets[i].windowTitle())
        self.stacker.setCurrentIndex(i)
        # self.widgets[i].update()


class WindowManager(QMainWindow):
    def __init__(self, widgets):
        super().__init__(None)
        self.stacker = QStackedWidget(self)
        self.widgets = [LoginNewAccountStacker(widgets, self)]
        for w in self.widgets:
            self.stacker.addWidget(w)
        # NO IDEA WHY THIS IS NEEDED BUT DON'T REMOVE
        # -------------------------------------------
        self.c_layout = QHBoxLayout()
        self.c_layout.addWidget(self.stacker)
        self.setLayout(self.c_layout)
        # -------------------------------------------
        self.set_page(0)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    # TODO update window naming so it actually works
    def set_page(self, i):
        self.setWindowTitle(self.widgets[i].windowTitle())
        self.stacker.setGeometry(self.widgets[i].geometry())
        self.setGeometry(self.widgets[i].geometry())
        self.stacker.setCurrentIndex(i)


class LogInSignUp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty('class', 'login-signup')
        self.draw()
        self.setWindowTitle("Helping Hands La Crosse")

    def draw(self):
        # TODO style this, she dumb ugly doe
        login = QPushButton("Login")
        login.clicked.connect(self.login_click)
        login.setProperty('class', 'login-btn')
        signup = QPushButton("Sign-Up")
        signup.clicked.connect(self.signup_click)
        signup.setProperty('class', 'signup-btn')
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(login)
        vbox.addWidget(signup)
        # self.setGeometry(0, 0, 300, 300)
        self.setLayout(vbox)

    # Set the GUI to the Login page
    # TODO potentially add close if something is breaking
    def login_click(self):
        self.parent().parent().set_page(1)

    # Set the GUI to the New Account page
    def signup_click(self):
        self.parent().parent().set_page(2)


# returns the resolution of the current system (width and height)
def screen_resolution():
    sizeObject = QDesktopWidget().screenGeometry(0)
    
    return sizeObject.width(), sizeObject.height()