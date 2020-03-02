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
		
		# set up the VBox
		self.calendar_data_hbox = QHBoxLayout()
		self.calendar_vbox = QVBoxLayout()
		self.data_vbox = QVBoxLayout()
		# self.calendar_data_hbox.addWidget(self.calendar)
		# self.calendar_data_hbox.addWidget(QLabel("Bep"))
		self.calendar_vbox.addWidget(self.calendar)
		self.build_form(self.data_vbox)
		self.calendar_data_hbox.addLayout(self.calendar_vbox)
		self.calendar_data_hbox.addLayout(self.data_vbox)
		self.setLayout(self.calendar_data_hbox)
		# self.home_vbox = QVBoxLayout()
		# self.hbox = QHBoxLayout()
		# self.vbox = QVBoxLayout()
		# # TODO finish setting up layout
		# self.hbox.addWidget(self.calendar)
		# self.build_form(self.vbox)
		# self.vbox.setAlignment(Qt.AlignCenter)
		# self.hbox.setAlignment(Qt.AlignCenter)
		# self.hbox.addLayout(self.vbox)
		#
		# # self.hbox.addStretch(.5)
		# # set up the layout
		# # self.home_vbox.addLayout(self.hbox)
		# self.setLayout(self.home_vbox)
		self.calendar.setMaximumWidth(900)
		self.calendar.setMaximumHeight(900)
		# TODO set geometry of the window correctly after adding the horizontal bar of tabs at the top
		# set the geometry of the window
		sys_width, sys_height = self.screen_resolution()
		self.x_coord = 0
		self.y_coord = 40
		self.width = sys_width
		self.height = sys_height
		self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)

		# TODO set calendar geometry correctly after adding the horizontal bar of tabs at the top
		# set the geometry of the calendar widget
		sys_width, sys_height = self.screen_resolution()
		self.x_coord_cal = 0
		self.y_coord_cal = 0
		self.cal_width = sys_width / 2
		self.cal_height = sys_height - 200
		self.calendar.setGeometry(self.x_coord_cal, self.y_coord_cal, self.cal_width, self.cal_height)

	# Build the form side of the calendar
	def build_form(self, vbox):
		user_type = cs.CURRENT_USER
		if (user_type == 'Guest'):

			vbox.addWidget(QLabel('frick'))
			vbox.addWidget(QLabel('sad'))


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
