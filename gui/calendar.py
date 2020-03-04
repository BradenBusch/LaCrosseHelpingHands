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
from functools import partial

try:
	from non_profit.gui.login import *
	from non_profit import constants as cs
except:
	from gui.login import *
	import constants as cs


# TODO handle approving requests somewhere, idk where we want that functionality to go

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

		self.tab_label = QLabel("Events")
		self.tab_label.setProperty('class', 'cal-label')
		self.tab_label.setFixedHeight(62)
		self.hbox_2.addWidget(self.tab_label)
		# create the two VBoxes to divide the screen into two columns
		self.vbox_1 = QVBoxLayout()
		self.vbox_2 = QVBoxLayout()

		# Create the tabs Widget and populate the tabs
		cs.CURRENT_DATE = self.calendar.selectedDate()  # TODO ------ do not delete this line, can be modified tho --------
		self.tabs = QTabWidget()
		self.tabs.setProperty('class', 'tab-layout')
		self.calendar.clicked.connect(partial(self.draw_tab, self.tabs))  # self.draw_tab(self.tabs))

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

	# If the selected date is not the same as the previous date, delete all the tabs
	def check_existing_tabs(self, tab_layout, day, month, year):
		if day != cs.CURRENT_DATE.day() or month != cs.CURRENT_DATE.month() or year != cs.CURRENT_DATE.year():
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(i)
		else:
			print('Same day')

	# Build the buttons for the tabs
	def build_tab_btns(self, tab_layout, label=None, event=None):
		tab_vbox = QVBoxLayout()
		# tab_vbox.setAlignment(Qt.AlignCenter)
		tab_btn_hbox = QHBoxLayout()
		if label is not None:
			tab_vbox.addWidget(label)
		# TODO add information layout here
		if event is not None:
			pass
		# TODO replace current tab with the create event gui
		create_event_btn = QPushButton("Create New Event")
		create_event_btn.clicked.connect(partial(self.create_event_form, tab_layout))
		create_event_btn.setProperty('class', 'normal-bar-btn')
		create_event_btn.setCursor(QCursor(Qt.PointingHandCursor))

		volunteer_btn = QPushButton("Volunteer")
		# self.volunteer_btn.clicked.connect()
		volunteer_btn.setProperty('class', 'normal-bar-btn')
		volunteer_btn.setCursor(QCursor(Qt.PointingHandCursor))

		make_donation_btn = QPushButton("Make Donation")
		# self.make_donation_btn.clicked.connect()
		make_donation_btn.setProperty('class', 'normal-bar-btn')
		make_donation_btn.setCursor(QCursor(Qt.PointingHandCursor))

		modify_event_btn = QPushButton("Modify Event")
		# self.modify_event_btn.clicked.connect()
		modify_event_btn.setProperty('class', 'normal-bar-btn')
		modify_event_btn.setCursor(QCursor(Qt.PointingHandCursor))

		delete_event_btn = QPushButton("Delete Event")
		# self.delete_event_btn.clicked.connect()
		delete_event_btn.setProperty('class', 'normal-bar-btn')
		delete_event_btn.setCursor(QCursor(Qt.PointingHandCursor))

		# Assign the correct buttons based on who's logged in
		print(cs.CURRENT_USER)
		if cs.CURRENT_USER != 'Guest' and cs.CURRENT_USER != 'Volunteer':
			tab_btn_hbox.addWidget(create_event_btn)
		if cs.CURRENT_USER == 'Volunteer':
			tab_btn_hbox.addWidget(volunteer_btn)
			tab_btn_hbox.addWidget(make_donation_btn)
		if cs.CURRENT_USER == 'Staff' or cs.CURRENT_USER == 'Administrator':
			tab_btn_hbox.addWidget(modify_event_btn)
			tab_btn_hbox.addWidget(delete_event_btn)

		tab_vbox.addLayout(tab_btn_hbox)
		tab = QWidget()
		tab.setLayout(tab_vbox)
		tab_layout.addTab(tab, "")

	def create_event_form(self, tab_layout):
		# Set up input fields
		for i in range(0, tab_layout.count()):
			tab_layout.removeTab(i)
		event_name = QLineEdit()
		event_location = QLineEdit()
		event_start_time = QComboBox()
		event_end_time = QComboBox()
		event_description = QTextEdit()
		event_volunteers_needed = QLineEdit()
		event_name.setPlaceholderText("Enter an Event Name")
		event_location.setPlaceholderText("Enter the Event Location")
		for i in range(24):
			if i < 12:
				hour_time = '0' + str(i) + ':00'
				half_hour_time = '0' + str(i) + ':30'
			else:
				hour_time = str(i) + ':00'
				half_hour_time = str(i) + ':30'
			event_start_time.addItem(hour_time)
			event_start_time.addItem(half_hour_time)
			event_end_time.addItem(hour_time)
			event_end_time.addItem(half_hour_time)
		event_description.setPlaceholderText("Describe the event")
		event_volunteers_needed.setPlaceholderText("Enter number of Volunteers needed as a number")

		# TODO verify will verify the information in the fields. When it is done it will call a function to repopulate
		#      the events being shown
		#  - Cancel will call the function that repopulates the events being shown
		# set up the confirm button

		form_list = [event_name, event_location, event_start_time, event_end_time, event_description, event_volunteers_needed]
		confirm_btn = QPushButton("Confirm")
		# confirm_btn.clicked.connect(partial(self.verify_fields, form_list))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
		# set up the cancel button
		cancel_btn = QPushButton("Cancel")
		# cancel_btn.clicked.connect(self.go_back)
		cancel_btn.setProperty('class', 'special-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))

		time_hbox = QHBoxLayout()
		time_hbox.addWidget(QLabel('Event Start Time'))
		time_hbox.addWidget(event_start_time)
		time_hbox.addWidget(QLabel('Event End Time'))
		time_hbox.addWidget(event_end_time)
		vbox = QVBoxLayout()
		vbox.addWidget(event_name)
		vbox.addWidget(event_location)
		vbox.addLayout(time_hbox)
		vbox.addWidget(event_description)
		vbox.addWidget(event_volunteers_needed)
		btn_hbox = QHBoxLayout()
		btn_hbox.addWidget(cancel_btn)
		btn_hbox.addWidget(confirm_btn)
		vbox.addLayout(btn_hbox)
		form = QWidget()
		form.setLayout(vbox)
		tab_layout.addTab(form, "Event Creation")

	# TODO make information showing window
	def show_events(self, tab_layout):
		pass

	# TODO handle when input isn't a number, add to database, no empty fields, isnt a day that hasnt happened, etc
	def verify_fields(self):
		pass

	# TODO create an actual layout for the tabs, based on what type of user they are
	# Build the tabs showing current events of the day
	def draw_tab(self, tab_layout):
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
		# No Events on this date, set as no events
		except Event.DoesNotExist:
			# Delete current tabs in the view, as current day doesn't have any
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(i)
			no_events = QLabel('No set events on this day')
			no_events.setProperty('class', 'cal-label')
			self.build_tab_btns(tab_layout, no_events)
			return
		# TODO update accordingly
		# for event_id in events_id:
		# 	event_details = Event.select(Event.event_id == event_id)
		# 	event_name = event_details.event_name
		# 	event_description = event_details.event_description
		# 	event_date_time = event_details.event_date

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
