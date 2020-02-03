'''
Top level program, starts the application.

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial

Authors: Alex, Braden, Kaelan
Version: 02/01/2020

'''

from PyQt5.QtWidgets import *

try:
    from non_profit.gui.login_signup import LogInSignUp
    from non_profit.models.database import connect
except:
    from gui.login_signup import LogInSignUp
    from models.database import connect


def main():
    app = QApplication([])
    # app.setStyleSheet() (we will do this later using QCSS, very similar to CSS and easy to use.
    connect()  # connect to the database

    current_window = LogInSignUp()  # start the application with the initial screen, the login screen.
    # Refactor this so that there is always a reference to a widget, or else it gets garbage collected.
    # We might have to setup a "storage" window, like a QStackedWidget or QMainWindow or something like that.
    # If a widget is closing immediately, its probably because it is losing its reference.

    # app.setActiveWindow(login_signup)
    app.exec_()


if __name__ == "__main__":
    main()
