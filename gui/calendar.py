'''
Holds the everything related to the calendar page.
Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/05/2020

'''

import calendar
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial

try:
	from non_profit.gui.homepage import *
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

		# set the maximum width of the calendar widget
		self.calendar.setMaximumWidth(sys_width // 2)

	# If the selected date is not the same as the previous date, delete all the tabs
	def check_existing_tabs(self, tab_layout, day, month, year):
		if day != cs.CURRENT_DATE.day() or month != cs.CURRENT_DATE.month() or year != cs.CURRENT_DATE.year():
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(0)

	# Check if the event a user is signing up for conflicts with an event they have already signed up for.
	def is_conflicting_event(self, event_id):
		user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		# print(f'User Events {user_events}s')
		event_ids = user_events.split(' ')
		check_event = Event.get(Event.id == event_id)
		# print('TEST Event Ids: ' + str(event_ids))
		# User is signed up for no events, impossible to conflict with other events
		if event_ids[0] == '-1':
			return False
		# Check each event the user is attending and check if it has conflicting time
		for event in event_ids:
			curr_event = Event.get(Event.id == event)
			e_year = curr_event.year
			e_month = curr_event.month
			e_day = curr_event.day
			e_start_time = curr_event.start_date
			e_end_time = curr_event.end_date
			e_s = datetime.strptime(e_start_time, '%H:%M')
			e_e = datetime.strptime(e_end_time, '%H:%M')
			c_e_s = datetime.strptime(check_event.start_date, '%H:%M')
			c_e_e = datetime.strptime(check_event.end_date, '%H:%M')
			# print(f'check_event_s {c_e_s} check_event_e {c_e_e} e_s {e_s} e_e {e_e}')  TODO use for debug
			if e_year == check_event.year:
				if e_month == check_event.month:
					if e_day == check_event.day:
						if self.time_in_range(e_s, e_e, c_e_s) or self.time_in_range(e_s, e_e, c_e_e):
							return True
						else:
							continue
					else:
						continue
				else:
					continue
			else:
				continue
		return False

	# Return true if time is in the range [start, end]
	def time_in_range(self, start, end, time):
		if start <= end:
			return start <= time <= end
		else:
			return start <= time or time <= end

	# Update the volunteer window when a volunteer volunteers for an event.
	def update_volunteer(self, tab_layout, event_id):
		# Get events volunteer ids
		volunteer_ids = Event.get(Event.id == event_id).volunteers_ids
		user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		# print(f'Volunteer ids: {volunteer_ids}')
		# print(f'Current User Events {user_events}s')
		# Check if the user has a conflicting event
		if self.is_conflicting_event(event_id):
			QMessageBox.about(None, " ", " You already have an event that conflicts with this event. ")
		else:
			# Get each id of the volunteer
			ids = volunteer_ids.split(' ')
			# Check if event is already full
			if Event.get(Event.id == event_id).volunteers_attending == Event.get(Event.id == event_id).volunteers_needed:
				QMessageBox.about(None, " ", " This event has max volunteers already. ")
			# First volunteer for the event
			elif volunteer_ids == '-1':
				new_ids = str(cs.CURRENT_USER_ID) + " "
				Event.update(volunteers_ids=new_ids).where(Event.id == event_id).execute()
				Event.update({Event.volunteers_attending: 1}).where(Event.id == event_id).execute()
				if user_events == '-1':
					user_events = str(event_id)
				else:
					user_events += ' ' + str(event_id)
				User.update({User.event_ids: user_events}).where(User.user_id == cs.CURRENT_USER_ID).execute()
				QMessageBox.about(None, " ", " You are now registered for this event. ")
			# No conflicting events, let user volunteer. Update the Event and User.
			else:
				# print(f'Current User Id {cs.CURRENT_USER_ID} volunteer ids: {volunteer_ids}s')
				# print(str(cs.CURRENT_USER_ID) + str(volunteer_ids))
				new_volunteer_num = len(ids)

				Event.update({Event.volunteers_attending: new_volunteer_num}).where(Event.id == event_id).execute()
				Event.update(volunteers_ids=volunteer_ids).where(Event.id == event_id).execute()
				if user_events == '-1':
					user_events = str(event_id)
				else:
					# TODO might need a space here
					user_events += ' ' + str(event_id)
				# print(f'User Events: {user_events}')
				User.update({User.event_ids: user_events}).where(User.user_id == cs.CURRENT_USER_ID).execute()
		self.draw_tab(tab_layout)
		# self.show_events(tab_layout)

	# Build the buttons for the tabs
	def build_tab_btns(self, tab_layout, label=None, event_vbox=None, event_id=None):
		tab_vbox = QVBoxLayout()
		# tab_vbox.setAlignment(Qt.AlignCenter)
		tab_btn_hbox = QHBoxLayout()
		if label is not None:
			label.setAlignment(Qt.AlignCenter)
			tab_vbox.addWidget(label)
		if event_vbox is not None:
			tab_vbox.addLayout(event_vbox)
		create_event_btn = QPushButton("Create New Event")
		create_event_btn.clicked.connect(partial(self.create_event_form, tab_layout))
		create_event_btn.setProperty('class', 'normal-bar-btn')
		create_event_btn.setCursor(QCursor(Qt.PointingHandCursor))

		volunteer_btn = QPushButton("Volunteer")
		if event_id is not None:
			volunteer_btn.clicked.connect(partial(self.update_volunteer, tab_layout, event_id))
		volunteer_btn.setProperty('class', 'normal-bar-btn')
		volunteer_btn.setCursor(QCursor(Qt.PointingHandCursor))

		make_donation_btn = QPushButton("Make Donation")
		if event_id is not None:
			make_donation_btn.clicked.connect(partial(self.create_donation_form, tab_layout, event_id))
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
		try:
			event_name = Event.get(Event.id == event_id).name
		except:
			event_name = None
		if event_id is None:
			tab_layout.addTab(tab, "")
		else:
			tab_layout.addTab(tab, event_name)

	# build the donate money form
	def create_donation_form(self, tab_layout, event_id=None):
		for i in range(tab_layout.count()):
			tab_layout.removeTab(0)

		dollar_label = QLabel("$")
		dollar_label.setProperty('class', 'bold-label')
		donation_field = QLineEdit()
		donation_field.setPlaceholderText("Enter a donation value as a number")

		donation_hbox = QHBoxLayout()
		donation_hbox.addWidget(dollar_label)
		donation_hbox.addWidget(donation_field)

		spacer_hbox = QHBoxLayout()
		spacer = QLabel("")
		spacer.setProperty('class', 'cal-bar-spacer-label')
		spacer_hbox.addWidget(spacer)

		btn_hbox = QHBoxLayout()
		confirm_btn = QPushButton("Confirm")
		confirm_btn.clicked.connect(partial(self.verify_donation, tab_layout, donation_field, event_id))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(partial(self.draw_tab, tab_layout))
		cancel_btn.setProperty('class', 'special-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn_hbox.addWidget(confirm_btn)
		btn_hbox.addWidget(cancel_btn)

		vbox = QVBoxLayout()
		vbox.addLayout(donation_hbox)
		vbox.addLayout(spacer_hbox)
		vbox.addLayout(btn_hbox)
		vbox.setAlignment(Qt.AlignCenter)

		form = QWidget()
		form.setLayout(vbox)
		tab_layout.addTab(form, "Event Donation")

	def verify_donation(self, tab_layout, amount, event_id=None):
		if amount.text() == "":
			QMessageBox.warning(None, " ", "You did not enter an amount!")
			return
		elif not amount.text().isdigit():
			QMessageBox.warning(None, " ", "Please enter only numbers (0-9)")
			return
		else:
			curr_donation = Event.get(Event.id == event_id).donations
			# print(f'current_donation {curr_donation} amount {amount.text()}') TODO use for debug
			curr_donation = curr_donation + int(amount.text())
			Event.update(donations=curr_donation).where(Event.id == event_id).execute()
		self.draw_tab(tab_layout)

	# Build the form for creating an event. Will add an event to the day that the user currently has selected on Calender
	def create_event_form(self, tab_layout):
		for i in range(tab_layout.count()):
			tab_layout.removeTab(0)

		event_name = QLineEdit()
		event_location = QLineEdit()
		event_start_time = QComboBox()
		event_end_time = QComboBox()
		event_description = QTextEdit()
		event_volunteers_needed = QLineEdit()
		event_name.setPlaceholderText("Enter an Event Name")
		event_location.setPlaceholderText("Enter the Event Location")
		for i in range(24):
			if i < 10:
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

		# Build the buttons
		form_list = [event_name, event_location, event_start_time, event_end_time, event_description, event_volunteers_needed]
		confirm_btn = QPushButton("Confirm")
		confirm_btn.clicked.connect(partial(self.verify_fields, form_list))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(partial(self.draw_tab, tab_layout))
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

	# Show all the information for each event on the currently selected day
	def show_events(self, tab_layout):
		date = self.calendar.selectedDate()
		day = date.day()
		month = date.month()
		year = date.year()
		events = Event.select().where(
			(Event.day == day) &
			(Event.month == month) &
			(Event.year == year))
		for event in events:
			vbox = QVBoxLayout()
			spacer = QLabel("")
			spacer.setProperty('class', "cal-bar-spacer-label")

			name_hbox = QHBoxLayout()
			name = QLabel('Name: ')
			name.setProperty('class', 'bold-label')
			name_hbox.addWidget(name)
			n = QLabel(event.name)
			n.setProperty('class', 'tab-info')
			name_hbox.addWidget(n)
			name_hbox.addWidget(spacer)

			location_hbox = QHBoxLayout()
			location = QLabel('Location: ')
			location.setProperty('class', 'bold-label')
			location_hbox.addWidget(location)
			loc = QLabel(event.location)
			loc.setProperty('class', 'tab-info')
			location_hbox.addWidget(loc)
			location_hbox.addWidget(spacer)
			
			date_hbox = QHBoxLayout()
			date = QLabel('Date: ')
			date.setProperty('class', 'bold-label')
			date_hbox.addWidget(date)
			time = "%s/%s/%s, %s-%s" % (event.month, event.day, event.year, event.start_date, event.end_date)
			t = QLabel(time)
			t.setProperty('class', 'tab-info')
			date_hbox.addWidget(t)
			date_hbox.addWidget(spacer)
			
			description_hbox = QHBoxLayout()
			description = QLabel('Description: ')
			description.setProperty('class', 'bold-label')
			description_hbox.addWidget(description)
			d = QLabel(event.description)
			d.setProperty('class', 'tab-info')
			d.setWordWrap(True)
			description_hbox.addWidget(d)
			description_hbox.addWidget(spacer)

			volunteer_hbox = QHBoxLayout()
			volunteer = QLabel('Volunteers: ')
			volunteer.setProperty('class', 'bold-label')
			volunteer_hbox.addWidget(volunteer)
			v = "%s / %s" % (str(event.volunteers_attending), str(event.volunteers_needed))
			vol = QLabel(v)
			vol.setProperty('class', 'tab-info')
			volunteer_hbox.addWidget(vol)
			volunteer_hbox.addWidget(spacer)

			donations_hbox = QHBoxLayout()
			donation = QLabel('Donations: ')
			donation.setProperty('class', 'bold-label')
			donations_hbox.addWidget(donation)
			donation_val = "$ " + str(event.donations)
			donation_lab = QLabel(donation_val)
			donation_lab.setProperty('class', 'tab-info')
			donations_hbox.addWidget(donation_lab)
			donations_hbox.addWidget(spacer)

			vbox.addLayout(name_hbox)
			vbox.addLayout(location_hbox)
			vbox.addLayout(date_hbox)
			vbox.addLayout(description_hbox)
			vbox.addLayout(volunteer_hbox)
			vbox.addLayout(donations_hbox)
			self.build_tab_btns(tab_layout, None, vbox, event.id)

	# [event_name, event_location, event_start_time, event_end_time, event_description, event_volunteers_needed]
	# Validate the input from 'Create Event' and store in the database if it is.
	def verify_fields(self, form_list):
		for i, field in enumerate(form_list):
			if i == 2 or i == 3 or i == 4:
				continue
			if field.text() == "":
				msg = QMessageBox.warning(None, " ", " You must fill all fields. ")
				return
		if not form_list[5].text().isdigit():
			msg = QMessageBox.warning(None, " ", " Your number of volunteers must be a number. ")
			form_list[5].clear()
			return

		event_start = str(form_list[2].currentText()).split(':')[0]
		event_end = str(form_list[3].currentText()).split(':')[0]
		if int(event_end) < int(event_start):
			msg = QMessageBox.warning(None, " ", " Your event start time must be before it's end time. ")
			return
		date = self.calendar.selectedDate()
		day = date.day()
		month = date.month()
		year = date.year()
		event_start_time = str(form_list[2].currentText())
		event_end_time = str(form_list[3].currentText())
		new_event = Event(day=day, month=month, year=year, start_date=event_start_time, end_date=event_end_time, name=form_list[0].text(), description=form_list[4].toPlainText(), location=form_list[1].text(), volunteers_needed=form_list[5].text(), volunteers_attending=0, volunteers_ids="-1", donations=0)
		new_event.save()
		self.draw_tab(self.tabs)

	# Build the tabs showing current events of the day
	def draw_tab(self, tab_layout):
		date = self.calendar.selectedDate()
		day = date.day()
		month = date.month()
		year = date.year()
		# self.check_existing_tabs(tab_layout, day, month, year)
		# Delete all tabs to then redraw them.
		for i in range(0, tab_layout.count()):
			tab_layout.removeTab(0)
		# Update the current date after the check has been performed
		cs.CURRENT_DATE = date

		# Check if there are events in the database on this day (this query will fail if there are no events this day)
		try:
			event = Event.get(
				(Event.day == day) &
				(Event.month == month) &
				(Event.year == year)).id

		# No Events on this date, set as no events
		except Event.DoesNotExist:
			# Delete current tabs in the view, as current day doesn't have any
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(0)
			no_events = QLabel('No set events on this day')
			no_events.setProperty('class', 'cal-label')
			self.build_tab_btns(tab_layout, no_events, None, None)
			return

		for i in range(0, tab_layout.count()):
			tab_layout.removeTab(0)
		self.show_events(tab_layout)

	# reset the day to the current day
	def reset_day(self):
		# determine the current date
		self.currentMonth = datetime.now().month
		self.currentYear = datetime.now().year
		self.currentDay = datetime.now().day

		# set the selected date as the current day
		self.calendar.setSelectedDate(QDate(self.currentYear, self.currentMonth, self.currentDay))

		# Remove tabs from the current day TODO remove me if necessary
		for i in range(0, self.tabs.count()):
			self.tabs.removeTab(0)

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
		self.reset_day()

	# go to the calendar page
	def cal_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CAL)
	
	# go to the about us page
	def about_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ABOUT)
		self.reset_day()

	# go to the contact us page
	def contact_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CONTACT)
		self.reset_day()

	# go to the search page
	def search_click(self):
		self.win.set_page(self.this_page, cs.PAGE_SEARCH)
		self.reset_day()

	# go to the account page
	def account_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ACCOUNT)
		self.reset_day()

	# return to the login signup screen
	def logout_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
		self.reset_day()

		# TODO actually log the user out of their account
		cs.CURRENT_USER = "Guest"
	
	# go to the login page
	def login_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN)
		self.reset_day()
	
	# go to the new account page
	def signup_click(self):
		self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
		self.reset_day()
	
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
