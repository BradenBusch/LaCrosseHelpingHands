'''
Window template, copy this file and rename it to create a new page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Homepage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set window title and properties, initialize the window reference
        self.setProperty('class', 'homepage')    # TODO set property name correctly
        self.setWindowTitle("Welcome!")    # TODO set window title correctly
        self.win = None
        
        # draw the page
        self.draw()
    
    # adds all buttons and sets up the layout
    def draw(self):
        # TODO style the button in 'non_profit_style.qss'
        btn_name = QPushButton("Button")    # TODO name button
        btn_name.clicked.connect(self.btn_click)    # TODO call button click method
        btn_name.setProperty('class', 'button-btn')    # TODO set button name correctly
        btn_name.setCursor(QCursor(Qt.PointingHandCursor))
        
        # TODO add more buttons here
        
        # TODO choose from the three layouts to form the layout of the window
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        
        # EXAMPLE:
        # define the VBox
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)    # TODO add "stretches" to create padding between buttons
        # vbox.addWidget(btn_name)
        # TODO add more button widgets to the vbox here
        
        # set up the layout
        self.setLayout(self.vbox)    # TODO set layout according to the layout chosen
        
        # set the geometry of the window    # TODO set geometry of the window correctly
        sys_width, sys_height = self.screen_resolution()
        self.x_coord = sys_width / 2
        self.y_coord = sys_height / 4
        self.width = 500
        self.height = 500
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
    
    # TODO add additional methods here
    
    # defines what happens when the button is clicked
    def btn_click(self):
        self.win.set_page(0)    # TODO perform correct action when button is clicked
    
    # TODO add additional button methods here
    
    # draws shapes on the window
    def paintEvent(self, e):
        painter = QPainter(self)
        
        # set the color and pattern of the border of the shape: (color, thickness, pattern)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))    # TODO set border properties
        
        # set the color and pattern of the shape: (r, g, b, alpha)
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))    # TODO set color
        
        # set the properties of the rectangle: (x-coord, y-coord, width, height)
        painter.drawRect(5, 200, 473, 275)    # TODO rectangle properties (or another shape)
    
    # resets the coordinates of the window after switching to this page
    def set_position(self):
        self.parent().move(self.x_coord, self.y_coord)
        self.parent().resize(self.width, self.height)
    
    # returns the resolution of the current system (width and height)
    def screen_resolution(self):
        # retrieve the resolution of the current system
        geometry = QDesktopWidget().screenGeometry(0)
        
        return geometry.width(), geometry.height()
