'''
Top level program, starts the application.

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial
PyQt5 Styling: https://doc.qt.io/qt-5/stylesheet-examples.html
PyQt5 Painting: http://zetcode.com/gui/pyqt5/painting/

Authors: Alex, Braden, Kaelan
Version: 02/05/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

try:
    from non_profit.models.database import *
    from non_profit.gui.login_signup import LogInSignUp
    from non_profit.gui.non_profit_style_driver import *
    from non_profit.gui.calendar import Calendar
    from non_profit.gui.gui_manager import *
except:
    from models.database import *
    from gui.login_signup import LogInSignUp
    from gui.non_profit_style_driver import *
    from gui.calendar import Calendar
    from gui_manager import *

try:
    from non_profit.gui.login_signup import *
except:
    from gui.login_signup import *


def main():
    app = QApplication([])
    app.setStyleSheet(style_sheet())
    db.connect(reuse_if_open=True)
    # db.drop_tables([User, Event])  # TODO uncomment me if you want all data deleted from the database
    db.create_tables([User, Event])
    # current_window = WindowManager([LogInSignUp(), Login(), NewAccount(), Calendar()])  # TODO add windows here
    current_window = Controller()

    width, height = screen_resolution()

    current_window.setMaximumWidth(width)
    current_window.setMaximumHeight(height)

    current_window.showMaximized()

    app.exec_()


# returns the resolution of the current system (width and height)
def screen_resolution():
    sizeObject = QDesktopWidget().screenGeometry(0)

    return sizeObject.width(), sizeObject.height()


if __name__ == "__main__":
    main()


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Window')

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def switch(self):
        self.switch_window.emit(self.line_edit.text())


class WindowTwo(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Window Two')
        self.setGeometry(0, 0, 1000, 1000)
        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)


class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.window.close()
        self.window_two.show()
