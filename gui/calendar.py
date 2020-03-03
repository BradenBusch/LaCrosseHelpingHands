'''
Holds the everything related to the calendar page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/02/2020

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
		self.setWindowTitle("Calendar")
		self.win = None
		
		# set the page id
		self.this_page = cs.PAGE_CAL
		
		# determine the current date
		self.currentMonth = datetime.now().month
		self.currentYear = datetime.now().year
		self.currentDay = datetime.now().day
		
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
		
		# set the selected date as the current day
		self.calendar.setSelectedDate(QDate(self.currentYear, self.currentMonth, self.currentDay))

		# self.calendar.clicked.connect(self.printDateInfo)
		# retrieve the resolution of the system
		sys_width, sys_height = self.screen_resolution()
		
		# set up the top level VBox
		self.vbox_screen = QVBoxLayout()
		
		# create the spacer for the bar of tabs
		self.hbox_1 = QHBoxLayout()
		self.spacer_1 = QLabel("")
		self.spacer_1.setProperty('class', 'cal-bar-spacer-label')
		self.hbox_1.addWidget(self.spacer_1)
		self.vbox_screen.addLayout(self.hbox_1)
		
		# create the top bar of tabs for the application
		self.top_bar()
		
		# create the HBoxes
		self.hbox_2 = QHBoxLayout()
		self.hbox_screen = QHBoxLayout()
		
		# create a label for the calendar page
		self.cal_label = QLabel("Calendar")
		self.cal_label.setProperty('class', 'cal-label')
		self.cal_label.setFixedHeight(62)
		self.hbox_2.addWidget(self.cal_label)
		
		# create the two VBoxes to divide the screen into two columns
		self.vbox_1 = QVBoxLayout()
		self.vbox_2 = QVBoxLayout()

		# Create the tabs Widget and populate the tabs
		cs.CURRENT_DATE = self.calendar.selectedDate()
		self.tabs = QTabWidget()
		self.tabs.setProperty('class', 'tab-layout')
		self.calendar.clicked.connect(self.draw_tab(self.tabs))

		# add the calendar and the tab widget that will display events
		self.vbox_1.addWidget(self.calendar)
		self.vbox_2.addWidget(self.tabs)

		# add the two VBoxes to the top level HBox
		self.hbox_screen.addLayout(self.vbox_1)
		self.hbox_screen.addLayout(self.vbox_2)
		
		# add the top level HBox to the top level VBox
		self.vbox_screen.addLayout(self.hbox_2)
		self.vbox_screen.addLayout(self.hbox_screen)
		
		# create the spacer for the bottom of the screen
		self.hbox_3 = QHBoxLayout()
		self.spacer_2 = QLabel("")
		self.spacer_2.setProperty('class', 'cal-bottom-spacer-label')
		self.hbox_3.addWidget(self.spacer_2)
		self.vbox_screen.addLayout(self.hbox_3)
		
		# set up the layout
		self.setLayout(self.vbox_screen)
		
		# set the geometry of the window
		self.x_coord = 0
		self.y_coord = 40
		self.width = sys_width
		self.height = sys_height
		self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
		
		# set the geometry of the calendar widget | NOTE: the vbox will actually resize the calendar widget on its own
		# self.x_coord_cal = 0
		# self.y_coord_cal = 0
		# self.cal_width = sys_width / 2
		# self.cal_width = 100
		# self.cal_height = sys_height - 200
		# self.calendar.setGeometry(self.x_coord_cal, self.y_coord_cal, self.cal_width, self.cal_height)
		
		# set the maximum width of the calendar widget
		self.calendar.setMaximumWidth(sys_width / 2)

	def check_existing_tabs(self, tab_layout, day, month, year):
		print(cs.CURRENT_DATE.day())
		if day != cs.CURRENT_DATE.day() or month != cs.CURRENT_DATE.month() or year != cs.CURRENT_DATE.year():
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(i)
		else:
			print('Same day')

	# TODO create an actual layout for the tabs, based on what type of user they are
	# Build the tabs showing current events of the day
	def draw_tab(self, tab_layout):
		def build_tab():
			date = self.calendar.selectedDate()
			day = date.day()
			month = date.month()
			year = date.year()
			self.check_existing_tabs(tab_layout, day, month, year)

			# Update the current date after the check has been performed
			cs.CURRENT_DATE = date

			# Get all events on this date
			try:
				events_id = Event.get(Event.event_id).where(
					(Event.event_date.day == day) &
					(Event.event_date.month == month) &
					(Event.event_date.year == year))
				print(events_id)
			# No Event(s) on this date
			except Event.DoesNotExist:
				for i in range(0, tab_layout.count()):
					tab_layout.removeTab(i)
				tab = QWidget()
				vbox = QVBoxLayout()
				vbox.addWidget(QLabel('No set events on this day'))
				vbox.setAlignment(Qt.AlignCenter)
				tab.setLayout(vbox)
				tab_layout.addTab(tab, "")

			# TODO uncomment when events are actually added
			# for event_id in events_id:
			# 	tab = QWidget()
			# 	vbox = QVBoxLayout()
			#
			# 	event_details = Event.select(Event.event_id == event_id)
			# 	event_name = event_details.event_name
			# 	event_description = event_details.event_description
			# 	event_date_time = event_details.event_date
			# 	vbox.addWidget(QLabel('hecc'))
			# 	tab.setLayout(vbox)
		return build_tab

	# creates the layout for the bar of tabs at the top of the application
	def top_bar(self):
		# set up the home button
		self.home_btn = QPushButton("Home")
		self.home_btn.clicked.connect(self.home_click)
		self.home_btn.setProperty('class', 'normal-bar-btn')
		self.home_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the calendar button
		self.cal_btn = QPushButton("Calendar")
		self.cal_btn.clicked.connect(self.cal_click)
		self.cal_btn.setProperty('class', 'normal-bar-btn')
		self.cal_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the about us button
		self.about_btn = QPushButton("About Us")
		self.about_btn.clicked.connect(self.about_click)
		self.about_btn.setProperty('class', 'normal-bar-btn')
		self.about_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the contact us button
		self.contact_btn = QPushButton("Contact Us")
		self.contact_btn.clicked.connect(self.contact_click)
		self.contact_btn.setProperty('class', 'normal-bar-btn')
		self.contact_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the search button
		self.search_btn = QPushButton("Search")
		self.search_btn.clicked.connect(self.search_click)
		self.search_btn.setProperty('class', 'normal-bar-btn')
		self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the account button (if the user is logged in)
		self.account_btn = QPushButton("Account")
		self.account_btn.clicked.connect(self.account_click)
		self.account_btn.setProperty('class', 'special-bar-btn')
		self.account_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the log out button (if the user is logged in)
		self.logout_btn = QPushButton("Log Out")
		self.logout_btn.clicked.connect(self.logout_click)
		self.logout_btn.setProperty('class', 'special-bar-btn')
		self.logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the sign up button (if the user is logged out)
		self.signup_btn = QPushButton("Sign Up")
		self.signup_btn.clicked.connect(self.signup_click)
		self.signup_btn.setProperty('class', 'special-bar-btn')
		self.signup_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the log in button (if the user is logged out)
		self.login_btn = QPushButton("Log In")
		self.login_btn.clicked.connect(self.login_click)
		self.login_btn.setProperty('class', 'special-bar-btn')
		self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# define the HBox
		self.hbox_bar = QHBoxLayout()
		
		# add all buttons to the HBox
		self.hbox_bar.addWidget(self.home_btn)
		self.hbox_bar.addWidget(self.cal_btn)
		# TODO add additional pages here
		self.hbox_bar.addWidget(self.about_btn)
		self.hbox_bar.addWidget(self.contact_btn)
		self.hbox_bar.addWidget(self.search_btn)
		self.hbox_bar.addWidget(QLabel(""))
		self.hbox_bar.addWidget(self.account_btn)
		self.hbox_bar.addWidget(self.logout_btn)
		self.hbox_bar.addWidget(self.signup_btn)
		self.hbox_bar.addWidget(self.login_btn)
		
		# check which type of user is logged in to determine what buttons will show up
		self.check_user()
		
		# add the HBox to the VBox
		self.vbox_screen.addLayout(self.hbox_bar)
	
	# go to the homepage
	def home_click(self):
		self.win.set_page(self.this_page, cs.PAGE_HOME)
	
	# go to the calendar page
	def cal_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CAL)
	
	# go to the about us page
	def about_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ABOUT)
	
	# go to the contact us page
	def contact_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CONTACT)
	
	# go to the search page
	def search_click(self):
		self.win.set_page(self.this_page, cs.PAGE_SEARCH)
	
	# go to the account page
	def account_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ACCOUNT)
	
	# return to the login signup screen
	def logout_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
		
		# TODO actually log the user out of their account
		cs.CURRENT_USER = "Guest"
	
	# go to the login page
	def login_click(self):
		self.win.set_page(cs.PAGE_CAL, cs.PAGE_LOGIN)
	
	# go to the new account page
	def signup_click(self):
		self.win.set_page(cs.PAGE_CAL, cs.PAGE_NEW_ACCOUNT)
	
	# TODO to be used for debugging
	def printDateInfo(self, qDate):
		print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
		print(f'Day Number of the year: {qDate.dayOfYear()}')
		print(f'Day Number of the week: {qDate.dayOfWeek()}')

	def get_date_info(self, qDate):
		return [qDate.month(), qDate.day(), qDate.year()]

	# draws shapes on the window
	def paintEvent(self, e):
		painter = QPainter(self)
		
		# set the color and pattern of the border of the shape: (color, thickness, pattern)
		painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
		
		# set the color and pattern of the shape: (r, g, b, alpha)
		painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
		
		# retrieve the resolution of the system
		sys_width, sys_height = self.screen_resolution()
		
		# set the properties of the rectangle: (x-coord, y-coord, width, height)
		painter.drawRect(0, 127, sys_width, 60)
	
	# resets the coordinates of the window after switching to this page
	def set_position(self):
		self.parent().move(self.x_coord, self.y_coord)
		self.parent().resize(self.width, self.height)
	
	# checks which user is logged in and formats the page to accomodate the user type
	def check_user(self):
		# check if the current user is a guest
		if cs.CURRENT_USER == "Guest":
			# show the signup and login buttons
			self.signup_btn.show()
			self.login_btn.show()
			
			# hide the account and logout buttons
			self.account_btn.hide()
			self.logout_btn.hide()
		
		# if the current user is not a guest
		else:
			# hide the signup and login buttons
			self.signup_btn.hide()
			self.login_btn.hide()
			
			# show the account and logout buttons
			self.account_btn.show()
			self.logout_btn.show()
		
		# check if the current user is a volunteer
		if cs.CURRENT_USER == "Volunteer":
			pass
		
		# check if the current user is a staff member
		if cs.CURRENT_USER == "Staff":
			pass
		
		# check if the current user is an administrator
		if cs.CURRENT_USER == "Administrator":
			pass
	
	# returns the resolution of the current system (width and height)
	def screen_resolution(self):
		# retrieve the resolution of the current system
		geometry = QDesktopWidget().screenGeometry(0)
		
		return geometry.width(), geometry.height()
