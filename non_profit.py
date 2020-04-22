'''
Top level script, starts the application.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/05/2020

PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
PyQt5 Tutorial: https://build-system.fman.io/pyqt5-tutorial
PyQt5 Styling: https://doc.qt.io/qt-5/stylesheet-examples.html
PyQt5 Layouts: http://zetcode.com/gui/pyqt5/layout/
PyQt5 Painting: http://zetcode.com/gui/pyqt5/painting/

'''

try:
    from non_profit.models.database import *
    from non_profit.gui.window_manager import *
    from non_profit.gui.login_signup import *
    from non_profit.gui.homepage import *
    from non_profit.gui.calendar import *
    from non_profit.gui.account import *
    # from non_profit.gui.about import *
    # from non_profit.gui.contact import *
    # from non_profit.gui.help import *
    # from non_profit.gui.search import *
    from non_profit.gui.non_profit_style_driver import *
except:
    from models.database import *
    from gui.window_manager import *
    from gui.login_signup import *
    from gui.homepage import *
    from gui.calendar import *
    from gui.account import *
    # from gui.about import *
    # from gui.contact import *
    # from gui.help import *
    # from gui.search import *
    from gui.non_profit_style_driver import *


# main method, starts the application
def main():
    # define the application
    app = QApplication([])
    
    # style the application by applying the style sheet
    app.setStyleSheet(style_sheet())
    
    # connect to the database
    db.connect(reuse_if_open=True)
    
    # check if the database will be erased upon application start-up
    # if cs.DELETE:
        # delete all data from the database
    # db.drop_tables([User, Event])
    # create the tables within the database
    db.create_tables([User, Event])
    events = Event.select()
    
    for e in events:
        print('{0}/{1}/{2} Volunteers: {3}'.format(e.month, e.day, e.year, e.volunteers_attending))
    
    # create the pages for the application within the WindowManager
    current_window = WindowManager([LogInSignUp(),
                                    Login(),
                                    NewAccount(),
                                    Homepage(),
                                    Calendar(),
                                    Account()])
                                    #About(),
                                    #Contact(),
                                    #Help(),
                                    #Search()])
    
    # retrieve the current system resolution
    sys_width, sys_height = screen_resolution()
    
    # set dimensions of the application
    current_window.setMaximumWidth(sys_width)
    current_window.setMaximumHeight(sys_height)
    
    # show the application in maximized mode
    current_window.showMaximized()
    
    # start the application
    app.exec_()


# returns the resolution of the current system (width and height)
def screen_resolution():
    # retrieve the resolution of the current system
    geometry = QDesktopWidget().screenGeometry(0)
    
    return geometry.width(), geometry.height()


if __name__ == "__main__":
    main()
