'''
Description
 
Authors: Alex, Braden, Kaelan
Date: 1/29/2020

'''

from PyQt5.QtWidgets import QApplication
from non_profit.gui.HomeScreen import HomeScreen
from non_profit.models.database import connect
import sys


def main():
    app = QApplication([])
    # app.setStyleSheet() (we will do this later using QCSS, very similar to CSS and easy to use.
    connect()  # connect to the database
    home = HomeScreen()  # start the application with the initial screen, the login screen.

    sys.exit(app.exec_()) #(not sure when we call this)


if __name__ == "__main__":
    main()
