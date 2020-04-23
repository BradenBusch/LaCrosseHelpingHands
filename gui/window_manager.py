'''
Manages the relationship between all of the different pages.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/21/2020

'''

import os
import ctypes

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    from non_profit import constants as cs
except:
    import constants as cs


class WindowManager(QMainWindow):
    def __init__(self, widgets):
        super().__init__(None)
        
        # set the window icon, if file exits else use the other one (handles path to the image)
        if os.path.isfile('gui\\photos\\hands_icon.png'):
            self.setWindowIcon(QIcon('gui\\photos\\hands_icon.png'))
        else:
            self.setWindowIcon(QIcon('non_profit\\gui\\photos\\hands_icon.png'))
        
        # if the user is running windows, change the taskbar icon
        try:
            # tell windows what process the application is under
            myappid = 'helping_hands'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass
        
        # retrieve the resolution of the system
        sys_width, sys_height = self.screen_resolution()
        
        # set the helping hands banner
        banner = QLabel(self)
        
        # if file exists else use the other one (handles path to the image)
        if os.path.isfile('gui\\photos\\helping_hands_banner.png'):
            pixmap = QPixmap('gui\\photos\\helping_hands_banner.png')
        else:
            pixmap = QPixmap('non_profit\\gui\\photos\\helping_hands_banner.png')
        
        scaled_height = int(pixmap.height() * (sys_width / pixmap.width()))
        pixmap = pixmap.scaled(sys_width, scaled_height, transformMode=Qt.SmoothTransformation)
        banner.setPixmap(pixmap)
        banner.resize(pixmap.width(), pixmap.height())
        
        # set up the stacker and add all pages as widgets
        self.stacker = QStackedWidget(self)
        self.widgets = widgets
        
        # add each page to the stacker and set the WindowManager for each page
        for page in self.widgets:
            self.stacker.addWidget(page)
            page.win = self
        
        # set the layout for the stack of pages
        self.c_layout = QHBoxLayout()
        self.c_layout.addWidget(self.stacker)
        self.setLayout(self.c_layout)
        
        # set the starting page to the login signup screen
        self.set_page(cs.PAGE_LOGIN_SIGNUP, cs.PAGE_LOGIN_SIGNUP)
    
    # sets the application to the indicated page
    def set_page(self, previous, page_num):
        # ensure the page exists
        if not page_num < len(self.widgets):
            return
        
        # ensure we are not on the current page
        if page_num != cs.CURRENT_PAGE:
            # set the previous page
            cs.PREV_PAGE = previous
            
            # set the new current page
            cs.CURRENT_PAGE = page_num
            
            # go to the indicated page and set page properties and geometry
            self.setWindowTitle(self.widgets[page_num].windowTitle())
            self.stacker.setGeometry(self.widgets[page_num].geometry())
            self.stacker.setCurrentIndex(page_num)
            self.widgets[page_num].set_position()
            self.widgets[page_num].check_user()
            
            # if navigating to the homepage, refresh the upcoming events
            if page_num == cs.PAGE_HOME:
                self.widgets[page_num].hide_previous(1)
                self.widgets[page_num].populate_all_events()
                self.widgets[page_num].hide_previous(2)
            
            # if naviagating to the calendar page, display events for the current day
            elif page_num == cs.PAGE_CAL:
                self.widgets[page_num].draw_tab(self.widgets[page_num].tabs)
            
            # if navigating to the account page, refresh the user events
            elif page_num == cs.PAGE_ACCOUNT:
                self.widgets[page_num].check_account()
                self.widgets[page_num].hide_previous()
                self.widgets[page_num].populate_user_events()
                self.widgets[page_num].set_account_info()
            
            # if navigating to the administrator privileges page, refresh all users and events
            elif page_num == cs.PAGE_PRIVILEGES:
                self.widgets[page_num].hide_previous()
                self.widgets[page_num].populate_all_users()
                self.widgets[page_num].populate_all_events()
            
            # if navigating to the search page, refresh the results
            elif page_num == cs.PAGE_SEARCH:
                self.widgets[page_num].hide_previous()
                self.widgets[page_num].populate_results()
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)

        return geometry.width(), geometry.height()
