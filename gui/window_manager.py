'''
Manages the relationship between all of the different pages.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ctypes

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
        
        # set up the menu bar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        
        # set up the exit button on the fileMenu
        exitButton = QAction(QIcon('gui\\photos\\application_exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
    
    # sets the application to the indicated page
    def set_page(self, page_num):
        # ensure the page exists
        if not page_num < len(self.widgets):
            return
        
        # go to the indicated page and set page properties and geometry
        self.setWindowTitle(self.widgets[page_num].windowTitle())
        self.stacker.setGeometry(self.widgets[page_num].geometry())
        self.stacker.setCurrentIndex(page_num)
        self.widgets[page_num].set_position()
