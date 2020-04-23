'''
Top level script, starts the application.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/21/2020

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
    # from non_profit.gui.privileges import *
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
    # from gui.privileges import *
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
    
    # delete all data from the database
    # db.drop_tables([User, Event, OrgEvent])

    # create the tables within the database
    db.create_tables([User, Event, OrgEvent])

    # create the La Crosse Helping Hands "event" if it doesn't already exist
    try:
        org = OrgEvent.get(OrgEvent.id == cs.ORG_ID)
    except:
        org = OrgEvent(name="La Crosse Helping Hands", donations=0)
        org.save()
    print(f'org id {org.id}')

    # create the pages for the application within the WindowManager
    current_window = WindowManager([LogInSignUp(),
                                    Login(),
                                    NewAccount(),
                                    Homepage(),
                                    Calendar(),
                                    Account()])
                                    #Privileges(),
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
