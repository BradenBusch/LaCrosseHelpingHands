'''
Holds the everything related to the calendar page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

import calendar
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
	from non_profit.gui.login import *
	from non_profit import constants as cs

except:
	from gui.login import *
	import constants as cs


class Calendar(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# set window title and properties, initialize the window reference
		self.setProperty('class', 'calendar')
		self.setWindowTitle("Calendar")
		self.win = None

		# determine the current date
		self.currentMonth = datetime.now().month
		self.currentYear = datetime.now().year

		# draw the page
		self.draw()

	# adds all buttons and sets up the layout
	def draw(self):
		# set up the calendar widget
		self.calendar = QCalendarWidget(self)
		self.calendar.setGridVisible(True)

		# set the minimum and maximum dates
		self.calendar.setMinimumDate(QDate(self.currentYear, self.currentMonth - 1, 1))
		self.calendar.setMaximumDate(QDate(self.currentYear, self.currentMonth + 1,
										   calendar.monthrange(self.currentYear, self.currentMonth)[1]))

		# set up each calendar date as a simplified type of button
		self.calendar.setSelectedDate(QDate(self.currentYear, self.currentMonth, 1))
		self.calendar.clicked.connect(self.printDateInfo)

		# retrieve the resolution of the system
		sys_width, sys_height = self.screen_resolution()

		# set up the top level VBox
		self.vbox_screen = QVBoxLayout()
		# TODO finish setting up layout

		# create the top bar of tabs for the application
		self.top_bar()

		# create the top level HBox
		self.hbox_screen = QHBoxLayout()
		self.hbox_3 = QHBoxLayout()

		# create the two VBoxes to divide the screen into two columns
		self.vbox_1 = QVBoxLayout()
		self.vbox_2 = QVBoxLayout()

		self.vbox_1.addWidget(self.calendar)
		# self.vbox_2.addStretch(1)
		self.vbox_2.addWidget(QLabel("Hello2"))
		# self.vbox_2.addStretch(1)
		self.hbox_3.addWidget(QLabel(""))

		# add the two VBoxesto the top level HBox
		self.hbox_screen.addLayout(self.vbox_1)
		self.hbox_screen.addLayout(self.vbox_2)

		# add the top level HBox to the top level VBox
		self.vbox_screen.addLayout(self.hbox_screen)
		self.vbox_screen.addLayout(self.hbox_3)
		# self.vbox_screen.addStretch(0.001)

		# set up the layout
		self.setLayout(self.vbox_screen)

		# TODO set geometry of the window correctly after adding the horizontal bar of tabs at the top
		# set the geometry of the window
		self.x_coord = 0
		self.y_coord = 40
		self.width = sys_width
		self.height = sys_height
		self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)

		# TODO set calendar geometry correctly after adding the horizontal bar of tabs at the top
		# set the geometry of the calendar widget
		self.x_coord_cal = 0
		self.y_coord_cal = 0
		self.cal_width = sys_width / 2
		self.cal_height = sys_height - 200
		self.calendar.setGeometry(self.x_coord_cal, self.y_coord_cal, self.cal_width, self.cal_height)
		self.calendar.setMaximumWidth(sys_width / 2)
		self.calendar.setMaximumHeight(sys_height - 200)

	# creates the layout for the bar of tabs at the top of the application
	def top_bar(self):
		# set up the ? button
		btn_name1 = QPushButton("Button")  # TODO name button
		btn_name1.clicked.connect(self.btn_click)  # TODO call button click method
		btn_name1.setProperty('class', 'bar-btn')  # TODO set button name correctly
		btn_name1.setCursor(QCursor(Qt.PointingHandCursor))

		# set up the ? button
		btn_name2 = QPushButton("Button")  # TODO name button
		btn_name2.clicked.connect(self.btn_click)  # TODO call button click method
		btn_name2.setProperty('class', 'bar-btn')  # TODO set button name correctly
		btn_name2.setCursor(QCursor(Qt.PointingHandCursor))

		# set up the ? button
		btn_name3 = QPushButton("Button")  # TODO name button
		btn_name3.clicked.connect(self.btn_click)  # TODO call button click method
		btn_name3.setProperty('class', 'bar-btn')  # TODO set button name correctly
		btn_name3.setCursor(QCursor(Qt.PointingHandCursor))

		# create list of buttons
		btn_list = [btn_name1, btn_name2, btn_name3]

		# define the HBox
		self.hbox_bar = QHBoxLayout()

		# add each button to the HBox
		for button in btn_list:
			self.hbox_bar.addWidget(button)

		# add the HBox to the VBox
		self.vbox_screen.addLayout(self.hbox_bar)

	# defines what happens when the button is clicked
	def btn_click(self):
		self.win.set_page(0)  # TODO perform correct action when button is clicked

	# TODO to be used for debugging
	def printDateInfo(self, qDate):
		print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
		print(f'Day Number of the year: {qDate.dayOfYear()}')
		print(f'Day Number of the week: {qDate.dayOfWeek()}')

	# resets the coordinates of the window after switching to this page
	def set_position(self):
		self.parent().move(self.x_coord, self.y_coord)
		self.parent().resize(self.width, self.height)

	# returns the resolution of the current system (width and height)
	def screen_resolution(self):
		# retrieve the resolution of the current system
		geometry = QDesktopWidget().screenGeometry(0)

		return geometry.width(), geometry.height()
