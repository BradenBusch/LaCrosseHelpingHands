'''
Holds the main calendar viewable by all users.

'''

from datetime import datetime
import calendar
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDesktopWidget, QStackedWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDesktopWidget, QLabel, QAction
from PyQt5.QtCore import QDate

try:
	import non_profit.gui.login
except:
	import gui.login
	# from gui.login import *

# TODO track what type of user is currently logged in, Guest will have 'None' so we can default to that

# TODO I don't really know what's going on in this script, it's a mess of stuff copy-pasted from other scripts

# TODO why does the windowbar disappear

class CalendarWindow(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setProperty('class', 'calendar')
		self.setWindowTitle("Calendar")
		self.widgets = [Calendar()]
		self.draw()
		self.update()
	
	def draw(self):
		self.stacker = QStackedWidget(self)
		for widget in self.widgets:
			self.stacker.addWidget(widget)
		# I have no idea why this works, but don't touch it.
		# --------------------------------------------------
		self.v = QVBoxLayout()
		self.v.addWidget(QWidget())
		self.v.addWidget(self.stacker)
		self.setLayout(self.v)
		# --------------------------------------------------


class Calendar(QWidget):
	global currentYear, currentMonth
	
	currentMonth = datetime.now().month
	currentYear = datetime.now().year

	def __init__(self):
		super().__init__()
		self.setProperty('class', 'calendar')
		self.setWindowTitle('Calendar')
		width, height = screen_resolution()
		self.setGeometry(0, 0, width/2 + 50, height)
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
