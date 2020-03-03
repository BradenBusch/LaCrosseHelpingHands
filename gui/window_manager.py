'''
Manages the relationship between all of the different pages.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

'''

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
        
        # set the window icon
        self.setWindowIcon(QIcon('gui\\photos\\hands_icon.png'))
        
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
        pixmap = QPixmap('gui\\photos\\helping_hands_banner.png')
        scaled_height = pixmap.height() * (sys_width / pixmap.width())
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
        
        # set the starting page to the login screen (the first page in the stack)
        self.set_page(0)
        
        # # set up the menu bar | NOTE: disabled the menu bar for now, it isn't really necessary
        # self.mainMenu = self.menuBar()
        # self.fileMenu = self.mainMenu.addMenu('File')
        # self.editMenu = self.mainMenu.addMenu('Edit')
        # self.viewMenu = self.mainMenu.addMenu('View')
        # self.searchMenu = self.mainMenu.addMenu('Search')
        # self.toolsMenu = self.mainMenu.addMenu('Tools')
        # self.helpMenu = self.mainMenu.addMenu('Help')
        #
        # # set up the exit button on the fileMenu
        # self.exitButton = QAction(QIcon('gui\\photos\\application_exit.png'), 'Exit', self)
        # self.exitButton.setShortcut('Ctrl+Q')
        # self.exitButton.setStatusTip('Exit application')
        # self.exitButton.triggered.connect(self.close)
        # self.fileMenu.addAction(self.exitButton)
    
    # sets the application to the indicated page
    def set_page(self, page_num):
        # ensure the page exists
        if not page_num < len(self.widgets):
            return
        
        # ensure we are not on the current page
        if page_num != cs.CURRENT_PAGE:
            # set the new current page
            cs.CURRENT_PAGE = page_num
            
            # go to the indicated page and set page properties and geometry
            self.setWindowTitle(self.widgets[page_num].windowTitle())
            self.stacker.setGeometry(self.widgets[page_num].geometry())
            self.stacker.setCurrentIndex(page_num)
            self.widgets[page_num].set_position()
            self.widgets[page_num].check_user()
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)

        return geometry.width(), geometry.height()
