'''
Top level program, starts the application.

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial

Authors: Alex, Braden, Kaelan
Version: 02/05/2020

'''

from PyQt5.QtWidgets import *

from non_profit.models.database import connect
from PyQt5.QtWidgets import QApplication
from non_profit.gui.login_signup import LogInSignUp

from non_profit.models.database import connect

try:
    from non_profit.gui.login_signup import *
    from non_profit.models.database import connect
except:
    from gui.login_signup import *
    from models.database import connect


def main():
    app = QApplication([])
    # app.setStyleSheet() (we will do this later using QCSS, very similar to CSS and easy to use.
    connect()  # connect to the database
    current_window = WindowManager([LogInSignUp(), Login(), NewAccount()])
    current_window.show()

    app.exec_()


if __name__ == "__main__":
    main()
