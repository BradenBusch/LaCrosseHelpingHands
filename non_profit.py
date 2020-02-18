'''
Top level program, starts the application.

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial

Authors: Alex, Braden, Kaelan
Version: 02/05/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

try:
    from non_profit.models.database import *
    from non_profit.gui.login_signup import LogInSignUp
except:
    from models.database import *
    from gui.login_signup import LogInSignUp

try:
    from non_profit.gui.login_signup import *
except:
    from gui.login_signup import *



def main():
    app = QApplication([])
    # app.setStyleSheet() (we will do this later using QCSS, very similar to CSS and easy to use.
    db.connect(reuse_if_open=True)
    db.create_tables([User, Event])
    # print(db.get_tables())
    current_window = WindowManager([LogInSignUp(), Login(), NewAccount()])  # TODO add windows here

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
