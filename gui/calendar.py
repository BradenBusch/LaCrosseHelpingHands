'''
Holds the main calendar viewable by all users.

'''

from datetime import datetime
import calendar
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDesktopWidget
from PyQt5.QtCore import QDate

try:
	import non_profit.gui.login
except:
	import gui.login
	# from gui.login import *

# TODO track what type of user is currently logged in, Guest will have 'None' so we can default to that


class Calendar(QWidget):
	global currentYear, currentMonth
	
	currentMonth = datetime.now().month
	currentYear = datetime.now().year

	def __init__(self):
		super().__init__()
		self.setProperty('class', 'calendar')
		self.setWindowTitle('Calendar')
		width, height = screen_resolution()
		self.setGeometry(0, 0, 1000, 1000)
		self.draw()
		# self.update()
	
	def draw(self):

		self.calendar = QCalendarWidget(self)
		# self.calendar.move(20, 20)
		self.calendar.setGridVisible(True)
		width, height = screen_resolution()
		self.calendar.setGeometry(0, 0, 1000, 1000)
		self.calendar.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
		self.calendar.setMaximumDate(QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
		
		self.calendar.setSelectedDate(QDate(currentYear, currentMonth, 1))
		
		self.calendar.clicked.connect(self.printDateInfo)
	
	def printDateInfo(self, qDate):
		print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
		print(f'Day Number of the year: {qDate.dayOfYear()}')
		print(f'Day Number of the week: {qDate.dayOfWeek()}')
		# print(config.current_user_type)

# returns the resolution of the current system (width and height)
def screen_resolution():
	sizeObject = QDesktopWidget().screenGeometry(0)
	
	return sizeObject.width(), sizeObject.height()
