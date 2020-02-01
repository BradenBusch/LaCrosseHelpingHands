'''
Top level program, starts the application.

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial

Authors: Alex, Braden, Kaelan
Version: 02/01/2020

'''

from PyQt5.QtWidgets import *
from gui.login import Login
from models.database import connect


def main():
    app = QApplication([])
    # app.setStyleSheet() (we will do this later using QCSS, very similar to CSS and easy to use.
    connect()  # connect to the database
    login = Login()  # start the application with the initial screen, the login screen.
    app.setActiveWindow(login)
    # sys.exit(app.exec_()) (not sure when we call this)
    
    label = QLabel('Hello World!')
    label.show()
    app.exec_()


if __name__ == "__main__":
    main()
