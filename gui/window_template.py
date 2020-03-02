'''
Window template, copy this file and rename it to create a new page.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: XX/XX/2020 TODO enter correct date

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class WindowTemplate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty('class', 'window_template')    # TODO set property name correctly
        self.setWindowTitle("Window Title")    # TODO set window title correctly
        self.widgets = []    # TODO add widgets to the window here
        self.draw()
    
    # places buttons in the window
    def draw(self):
        # TODO style the button in 'non_profit_style.qss'
        btn_name = QPushButton("Button")    # TODO name button
        btn_name.clicked.connect(self.btn_click)    # TODO call button click method
        btn_name.setProperty('class', 'button-btn')    # TODO set button name correctly
        btn_name.setCursor(QCursor(Qt.PointingHandCursor))
        btn_name.resize(100, 100)
        btn_name.move(100, 0)
        
        
        btn_name1 = QPushButton("Button")  # TODO name button
        btn_name1.clicked.connect(self.btn_click)  # TODO call button click method
        btn_name1.setProperty('class', 'button-btn')  # TODO set button name correctly
        btn_name1.setCursor(QCursor(Qt.PointingHandCursor))

        #self.createTopLeftGroupBox()

        # mainLayout = QGridLayout()
        # define the number of rows and columns in the layout
        
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        
        # self.setLayout(mainLayout)
        
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(btn_name)
        # hbox.addWidget(btn_name1)
        #
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        #
        # self.setLayout(vbox)
        
        # TODO add more buttons here
        
        # define the VBox
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)    # TODO add "stretches" to create padding between buttons
        # vbox.addWidget(btn_name)
        
        # TODO add more button widgets to the vbox here
        
        width, height = screen_resolution()
        self.setGeometry(0, 0, width, height)
        
        # define the layout set up by the VBox
        #self.setLayout(vbox)
    
    # defines what happens when the button is clicked
    def btn_click(self):
        self.parent().parent().set_page(1)    # TODO perform correct action when button is clicked
        
        '''
        To go to page within the same stacker:
            self.parent().parent().set_page(1)
        
        To go to page in another stacker:
            self.parent().parent().win.set_page(1)
        '''
    
    # draws shapes on the window
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))    # TODO rectangle color (r, g, b, alpha)
        painter.drawRect(5, 200, 473, 275)    # TODO rectangle properties (x-coord, y-coord, width, height)
    
    
    
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)


# returns the resolution of the current system (width and height)
def screen_resolution():
    # retrieve the resolution of the current system
    geometry = QDesktopWidget().screenGeometry(0)
    
    return geometry.width(), geometry.height()
