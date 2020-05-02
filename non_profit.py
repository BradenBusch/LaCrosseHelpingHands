'''
Top level class, starts the application.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/23/2020

'''

try:
    from non_profit.models.database import *
    from non_profit.gui.window_manager import *
    from non_profit.gui.login_signup import *
    from non_profit.gui.login import *
    from non_profit.gui.new_account import *
    from non_profit.gui.homepage import *
    from non_profit.gui.calendar import *
    from non_profit.gui.account import *
    from non_profit.gui.privileges import *
    from non_profit.gui.about import *
    from non_profit.gui.contact import *
    from non_profit.gui.help import *
    from non_profit.gui.search import *
    from non_profit.gui.non_profit_style_driver import *
except:
    from models.database import *
    from gui.window_manager import *
    from gui.login_signup import *
    from gui.login import *
    from gui.new_account import *
    from gui.homepage import *
    from gui.calendar import *
    from gui.account import *
    from gui.privileges import *
    from gui.about import *
    from gui.contact import *
    from gui.help import *
    from gui.search import *
    from gui.non_profit_style_driver import *


class NonProfit():
    def __init__(self):
        # define the application
        self.app = QApplication([])
        
        # style the application by applying the style sheet
        self.app.setStyleSheet(style_sheet())
        
        # connect to the database
        db.connect(reuse_if_open=True)
        
        # delete all data from the database
        # db.drop_tables([User, Event, OrgEvent])

        # create the tables within the database
        db.create_tables([User, Event, OrgEvent])

        # create the La Crosse Helping Hands "event" if it doesn't already exist
        try:
            org = OrgEvent.get(OrgEvent.id == cs.ORG_ID)
        except OrgEvent.DoesNotExist:
            org = OrgEvent(name="La Crosse Helping Hands", donations=0)
            org.save()
        try:
            root_admin = User.get(User.user_id == cs.ROOT_ADMIN_ID)
        except User.DoesNotExist:
            root_admin_pass = hash_password(cs.ROOT_ADMIN_PASSWORD)
            root_admin = User(
                 username=cs.ROOT_ADMIN_USERNAME, password=root_admin_pass, account_email="", account_type="Administrator",
                 event_ids="-1", volunteer_hours=0.0, total_donations=0
            )
            root_admin.save()

        # create the pages for the application within the WindowManager
        self.current_window = WindowManager([LogInSignUp(),
                                             Login(),
                                             NewAccount(),
                                             Homepage(),
                                             Calendar(),
                                             Account(),
                                             Privileges(),
                                             About(),
                                             Contact(),
                                             Help(),
                                             Search()])
        
        # retrieve the current system resolution
        sys_width, sys_height = self.screen_resolution()
        
        # set dimensions of the application
        self.current_window.setMaximumWidth(sys_width)
        self.current_window.setMaximumHeight(sys_height)
        
        # show the application in maximized mode
        self.current_window.showMaximized()
        
        # start the application
        self.app.exec_()
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)
        
        return geometry.width(), geometry.height()


if __name__ == "__main__":
    NonProfit()
