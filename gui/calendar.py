'''
Calendar page of the application, has a calendar that allows users to register for events
and donate money to the organization.

Accessibile by: Guest, Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/23/2020

'''

import calendar
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial

try:
	from non_profit.models.database import *
	from non_profit import constants as cs
except:
	from models.database import *
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
		
		# restricts user input to integers only
		self.onlyInt = QIntValidator()
		
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
		cs.CURRENT_DATE = self.calendar.selectedDate()
		self.tabs = QTabWidget()
		self.tabs.setProperty('class', 'tab-layout')
		self.calendar.clicked.connect(partial(self.draw_tab, self.tabs))
		self.draw_tab(self.tabs)
		
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

	# Update the users total volunteer hours (hours += [end_time - start_time])
	def update_user_volunteer_hours(self, start_time, end_time):
		user_time = User.get(User.user_id == cs.CURRENT_USER_ID).volunteer_hours
		s_time = start_time.split(':')
		e_time = end_time.split(':')
		hour = int(e_time[0]) - int(s_time[0])
		if int(s_time[1]) > int(e_time[1]):  # Have to carry the minutes
			hour -= 1
			minute = .5
		else:  # No carrying needed, just subtract
			minute = int(e_time[1]) - int(s_time[1])
			if minute == 30:
				minute = .5
			else:
				minute = 0
		event_hours = float(hour) + float(minute)

		total_hours = float(event_hours) + float(user_time)
		User.update({User.volunteer_hours: total_hours}).where(User.user_id == cs.CURRENT_USER_ID).execute()
	
	# Update the volunteer window when a volunteer volunteers for an event.
	def update_volunteer(self, tab_layout, event_id):
		# Get events volunteer ids
		volunteer_ids = Event.get(Event.id == event_id).volunteers_ids
		user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids

		# Get times
		event_start = Event.get(Event.id == event_id).start_date
		event_end = Event.get(Event.id == event_id).end_date

		# Check if the user has a conflicting event
		if self.is_conflicting_event(event_id):
			QMessageBox.about(self, " ", " You are already registered for another event that conflicts with this event! ")
		else:
			# Get each id of the volunteer
			ids = volunteer_ids.split(' ')
			# Check if event is already full
			if Event.get(Event.id == event_id).volunteers_attending == Event.get(Event.id == event_id).volunteers_needed:
				QMessageBox.about(self, " ", " This event already has the maximum number of volunteers. ")
			# First volunteer for the event
			elif volunteer_ids == '-1':
				new_ids = str(cs.CURRENT_USER_ID) + " "
				Event.update(volunteers_ids=new_ids).where(Event.id == event_id).execute()
				Event.update({Event.volunteers_attending: 1}).where(Event.id == event_id).execute()
				if user_events == '-1':
					user_events = str(event_id)
				else:
					user_events += ' ' + str(event_id)
				# Update users events and hours
				User.update({User.event_ids: user_events}).where(User.user_id == cs.CURRENT_USER_ID).execute()
				self.update_user_volunteer_hours(event_start, event_end)
				QMessageBox.about(self, " ", " You are now registered for this event. ")
			# No conflicting events, let user volunteer. Update the Event and User.
			else:
				new_volunteer_num = len(ids)
				volunteer_ids += str(cs.CURRENT_USER_ID) + ' '
				Event.update({Event.volunteers_attending: new_volunteer_num}).where(Event.id == event_id).execute()
				Event.update(volunteers_ids=volunteer_ids).where(Event.id == event_id).execute()
				if user_events == '-1':
					user_events = str(event_id)
				else:
					user_events += ' ' + str(event_id)
				# Update the users events and hours
				User.update({User.event_ids: user_events}).where(User.user_id == cs.CURRENT_USER_ID).execute()
				self.update_user_volunteer_hours(event_start, event_end)
				QMessageBox.about(self, " ", " You are now registered for this event. ")
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
		self.create_event_btn = QPushButton("Create New Event")
		self.create_event_btn.clicked.connect(partial(self.create_event_form, tab_layout))
		self.create_event_btn.setProperty('class', 'normal-bar-btn')
		self.create_event_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the volunteer button
		self.volunteer_btn = QPushButton("Volunteer")
		if event_id is not None:
			self.volunteer_btn.clicked.connect(partial(self.update_volunteer, tab_layout, event_id))
		self.volunteer_btn.setProperty('class', 'normal-bar-btn')
		self.volunteer_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the donation button
		self.make_donation_btn = QPushButton("Donate")
		if event_id is not None:
			self.make_donation_btn.clicked.connect(partial(self.create_donation_form, tab_layout, event_id))
		self.make_donation_btn.setProperty('class', 'normal-bar-btn')
		self.make_donation_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the modify event button
		self.modify_event_btn = QPushButton("Modify Event")
		if event_id is not None:
			self.modify_event_btn.clicked.connect(partial(self.modify_event, tab_layout, event_id))
		self.modify_event_btn.setProperty('class', 'normal-bar-btn')
		self.modify_event_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# set up the delete event button
		self.delete_event_btn = QPushButton("Delete Event")
		if event_id is not None:
			self.delete_event_btn.clicked.connect(partial(self.delete_event, tab_layout, event_id))
		self.delete_event_btn.setProperty('class', 'normal-bar-btn')
		self.delete_event_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		date = self.calendar.selectedDate()
		day = date.day()
		month = date.month()
		year = date.year()
		
		# add appropriate buttons depending on which user is logged in
		if cs.CURRENT_USER == 'Volunteer':
			tab_btn_hbox.addWidget(self.volunteer_btn)
			tab_btn_hbox.addWidget(self.make_donation_btn)
		if cs.CURRENT_USER == 'Staff' or cs.CURRENT_USER == 'Administrator':
			tab_btn_hbox.addWidget(self.volunteer_btn)
			tab_btn_hbox.addWidget(self.make_donation_btn)
			tab_btn_hbox.addWidget(self.create_event_btn)
			tab_btn_hbox.addWidget(self.modify_event_btn)
			tab_btn_hbox.addWidget(self.delete_event_btn)
		
		# check if the date is valid
		if not self.date_valid(day, month, year):
			try:
				self.volunteer_btn.hide()
				self.make_donation_btn.hide()
			except:
				pass
			try:
				self.create_event_btn.hide()
				self.modify_event_btn.hide()
				self.delete_event_btn.hide()
			except:
				pass
		
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
		# remove all tabs
		for i in range(tab_layout.count()):
			tab_layout.removeTab(0)
		
		# set up donation field
		dollar_label = QLabel("$")
		dollar_label.setProperty('class', 'bold-label')
		donation_field = QLineEdit()
		donation_field.setPlaceholderText("Enter a donation amount")
		donation_field.setValidator(self.onlyInt)
		donation_field.setMaxLength(4)
		
		# set up layouts
		donation_hbox = QHBoxLayout()
		donation_hbox.addWidget(dollar_label)
		donation_hbox.addWidget(donation_field)
		
		spacer_hbox = QHBoxLayout()
		spacer = QLabel("")
		spacer.setProperty('class', 'cal-bar-spacer-label')
		spacer_hbox.addWidget(spacer)
		
		# set up buttons
		btn_hbox = QHBoxLayout()
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(partial(self.draw_tab, tab_layout))
		cancel_btn.setProperty('class', 'red-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		confirm_btn = QPushButton("Confirm")
		confirm_btn.clicked.connect(partial(self.verify_donation, tab_layout, donation_field, event_id))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn_hbox.addWidget(cancel_btn)
		btn_hbox.addWidget(confirm_btn)
		
		# set up layouts
		vbox = QVBoxLayout()
		vbox.addLayout(donation_hbox)
		vbox.addLayout(spacer_hbox)
		vbox.addLayout(btn_hbox)
		vbox.setAlignment(Qt.AlignCenter)
		
		# build form
		form = QWidget()
		form.setLayout(vbox)
		tab_layout.addTab(form, "Event Donation")
	
	# verify that the donation is valid
	def verify_donation(self, tab_layout, amount, event_id=None):
		# User did not enter an amount
		if amount.text() == "":
			QMessageBox.warning(self, " ", "You did not enter an amount!")
			return
		# User entered a negative amount
		elif int(amount.text()) <= 0:
			QMessageBox.warning(self, " ", "You did not enter a valid amount!")
			amount.clear()
			return
		# Update the user and event with the donation amount
		else:
			curr_donation = Event.get(Event.id == event_id).donations
			user_donations = User.get(User.user_id == cs.CURRENT_USER_ID).total_donations
			curr_donation = curr_donation + int(amount.text())
			user_donations = user_donations + int(amount.text())
			Event.update(donations=curr_donation).where(Event.id == event_id).execute()
			User.update(total_donations=user_donations).where(User.user_id == cs.CURRENT_USER_ID).execute()
			QMessageBox.about(self, " ", "Thank you for the donation!")
		self.draw_tab(tab_layout)
	
	# Build the form for creating an event. Will add an event to the day that the user currently has selected on Calendar
	def create_event_form(self, tab_layout):
		for i in range(tab_layout.count()):
			tab_layout.removeTab(0)
		
		event_name = QLineEdit()
		event_location = QLineEdit()
		event_start_time = QComboBox()
		event_end_time = QComboBox()
		event_description = QTextEdit()
		event_volunteers_needed = QLineEdit()
		event_volunteers_needed.setValidator(self.onlyInt)
		event_name.setPlaceholderText("Enter the Event Name")
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
		event_description.setPlaceholderText("Enter the Event Description")
		event_volunteers_needed.setPlaceholderText("Enter the number of Volunteers needed")
		
		# Build the buttons
		form_list = [event_name, event_location, event_start_time, event_end_time, event_description, event_volunteers_needed]
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(partial(self.draw_tab, tab_layout))
		cancel_btn.setProperty('class', 'red-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		confirm_btn = QPushButton("Confirm")
		confirm_btn.clicked.connect(partial(self.verify_fields, form_list, None))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
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
	def verify_fields(self, form_list, event_id=None):
		for i, field in enumerate(form_list):
			if i == 2 or i == 3 or i == 4:
				continue
			if field.text() == "":
				msg = QMessageBox.warning(self, " ", " You must fill all fields! ")
				return
		if not form_list[5].text().isdigit():
			msg = QMessageBox.warning(self, " ", " The number of volunteers must be a number. ")
			form_list[5].clear()
			return
		
		event_start = str(form_list[2].currentText()).split(':')[0]
		event_end = str(form_list[3].currentText()).split(':')[0]
		if int(event_end) < int(event_start):
			msg = QMessageBox.warning(self, " ", " The event start time must be before its end time. ")
			return
		date = self.calendar.selectedDate()
		day = date.day()
		month = date.month()
		year = date.year()
		event_start_time = str(form_list[2].currentText())
		event_end_time = str(form_list[3].currentText())
		# Update an Event
		if event_id is not None:
			old_event = Event.get(Event.id == event_id)
			if old_event.volunteers_needed > int(form_list[5].text()):
				QMessageBox.warning(self, " ", 'The new "volunteers needed" number must be equal to or greater than the old value. ')
				return
			old_event.name = form_list[0].text()
			old_event.description = form_list[4].toPlainText()
			old_event.location = form_list[1].text()
			old_event.volunteers_needed = int(form_list[5].text())
			old_event.start_date = event_start_time
			old_event.end_date = event_end_time
			old_event.save()
			QMessageBox.about(self, " ", " You successfully updated this event. ")
		# Create a new Event
		else:
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
			
			# show appropriate buttons depending on what user is logged in
			self.format_buttons(False, day, month, year)
		
		# No Events on this date, set as no events
		except Event.DoesNotExist:
			# Delete current tabs in the view, as current day doesn't have any
			for i in range(0, tab_layout.count()):
				tab_layout.removeTab(0)
			no_events = QLabel('No events scheduled on this day!')
			no_events.setProperty('class', 'cal-label')
			self.build_tab_btns(tab_layout, no_events, None, None)
			self.format_buttons(True, day, month, year)  # hide all buttons on days that have no events
			return
		
		for i in range(0, tab_layout.count()):
			tab_layout.removeTab(0)
		self.show_events(tab_layout)
	
	# formats the event buttons depending on which user is logged in
	def format_buttons(self, hide, day, month, year):
		# if all buttons are to be hidden
		if hide:
			# hide the buttons that need to be hidden
			try:
				self.volunteer_btn.hide()
			except:
				pass
			try:
				self.make_donation_btn.hide()
			except:
				pass
			try:
				if not (cs.CURRENT_USER == "Staff" or cs.CURRENT_USER == "Administrator"):
					self.create_event_btn.hide()
				if not self.date_valid(day, month, year):
					self.create_event_btn.hide()
			except:
				pass
			try:
				self.modify_event_btn.hide()
			except:
				pass
			try:
				self.delete_event_btn.hide()
			except:
				pass
		
		# if specific buttons need to be shown
		else:
			# check if the current user is a guest or if the date is invalid
			if cs.CURRENT_USER == "Guest" or not self.date_valid(day, month, year):
				# hide the buttons that need to be hidden
				try:
					self.volunteer_btn.hide()
				except:
					pass
				try:
					self.make_donation_btn.hide()
				except:
					pass
				try:
					self.create_event_btn.hide()
				except:
					pass
				try:
					self.modify_event_btn.hide()
				except:
					pass
				try:
					self.delete_event_btn.hide()
				except:
					pass
				return
			
			# check if the current user is a volunteer
			if cs.CURRENT_USER == "Volunteer":
				# hide the buttons that need to be hidden
				self.create_event_btn.hide()
				self.modify_event_btn.hide()
				self.delete_event_btn.hide()
				
				# show the buttons that need to be shown
				if self.date_valid(day, month, year):
					self.volunteer_btn.show()
					self.make_donation_btn.show()
			
			# check if the current user is a staff member
			if cs.CURRENT_USER == "Staff" or cs.CURRENT_USER == "Administrator":
				# show the buttons that need to be shown
				self.create_event_btn.show()
				
				if self.date_valid(day, month, year):
					self.volunteer_btn.show()
					self.make_donation_btn.show()
					self.modify_event_btn.show()
					self.delete_event_btn.show()
	
	# determines if the selected date occurs before the current date
	def date_valid(self, day, month, year):
		if year < self.currentYear:
			return False
		elif (month < self.currentMonth) and (year <= self.currentYear):
			return False
		elif (day < self.currentDay) and (month <= self.currentMonth):
			return False
		else:
			return True
	
	# reset the day to the current day
	def reset_day(self):
		# determine the current date
		self.currentMonth = datetime.now().month
		self.currentYear = datetime.now().year
		self.currentDay = datetime.now().day
		
		# set the selected date as the current day
		self.calendar.setSelectedDate(QDate(self.currentYear, self.currentMonth, self.currentDay))
		
		# Remove tabs from the current day
		for i in range(0, self.tabs.count()):
			self.tabs.removeTab(0)
		
		self.draw_tab(self.tabs)
	
	# modify a volunteering event. This will update the User and Event tables.
	def modify_event(self, tab_layout, event_id):
		# Get events information
		event = Event.get(Event.id == event_id)

		for i in range(tab_layout.count()):
			tab_layout.removeTab(0)
		# Make the fields
		event_name = QLineEdit()
		event_location = QLineEdit()
		event_start_time = QComboBox()
		event_end_time = QComboBox()
		event_description = QTextEdit()
		event_volunteers_needed = QLineEdit()
		event_volunteers_needed.setValidator(self.onlyInt)
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

		# Set the fields to their current values in the database
		event_name.setText(event.name)
		event_location.setText(event.location)
		start_index = event_start_time.findText(event.start_date, Qt.MatchFixedString)
		end_index = event_end_time.findText(event.end_date, Qt.MatchFixedString)
		if start_index >= 0 and end_index >= 0:
			event_start_time.setCurrentIndex(start_index)
			event_end_time.setCurrentIndex(end_index)
		event_description.setText(event.description)
		event_volunteers_needed.setText(str(event.volunteers_needed) + ' (the new value must be equal to or greater than the current value)')

		# Build the buttons
		form_list = [event_name, event_location, event_start_time, event_end_time, event_description, event_volunteers_needed]
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(partial(self.draw_tab, tab_layout))
		cancel_btn.setProperty('class', 'red-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		confirm_btn = QPushButton("Confirm")
		confirm_btn.clicked.connect(partial(self.verify_fields, form_list, event_id))
		confirm_btn.setProperty('class', 'normal-bar-btn')
		confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))

		# Build labels and add all widgets
		name_hbox = QHBoxLayout()
		name_hbox.addWidget(QLabel('Name:             '))
		name_hbox.addWidget(event_name)
		loc_hbox = QHBoxLayout()
		loc_hbox.addWidget(QLabel('Location:          '))
		loc_hbox.addWidget(event_location)
		time_hbox = QHBoxLayout()
		time_hbox.addWidget(QLabel('Event Start Time'))
		time_hbox.addWidget(event_start_time)
		time_hbox.addWidget(QLabel('Event End Time'))
		time_hbox.addWidget(event_end_time)
		vol_hbox = QHBoxLayout()
		vol_hbox.addWidget(QLabel('Needed Volunteers: '))
		vol_hbox.addWidget(event_volunteers_needed)

		vbox = QVBoxLayout()
		vbox.addLayout(name_hbox)
		vbox.addLayout(loc_hbox)
		vbox.addLayout(time_hbox)
		vbox.addWidget(QLabel("Description:"))
		vbox.addWidget(event_description)
		vbox.addLayout(vol_hbox)
		btn_hbox = QHBoxLayout()
		btn_hbox.addWidget(cancel_btn)
		btn_hbox.addWidget(confirm_btn)
		vbox.addLayout(btn_hbox)

		form = QWidget()
		form.setLayout(vbox)
		tab_layout.addTab(form, "Event Modification")

	# helper method to determine the length of an event
	def get_event_runtime(self, event):
		s_time = event.start_date
		e_time = event.end_date
		start = s_time.split(':')
		end = e_time.split(':')
		if start[1] == '30':
			s_min = 0.5
		else:
			s_min = 0.0
		if end[1] == '30':
			e_min = 0.5
		else:
			e_min = 0.0
		end_total = float(end[0]) + e_min
		start_total = float(start[0]) + s_min
		return end_total - start_total

	# hard delete a volunteering event. this will delete the event and update the users attached
	def delete_event(self, tab_layout, event_id):
		del_event = Event.get(Event.id == event_id)
		volunteer_ids = del_event.volunteers_ids
		volunteer_ids = volunteer_ids.split(' ')
		# This method will do the actual deleting
		self.update_all_volunteer_hours(volunteer_ids, del_event)
		# Redraw tabs
		self.draw_tab(tab_layout)

	# update each user affected by deletion of an event, then delete the event
	def update_all_volunteer_hours(self, volunteer_ids, event):
		# No volunteers were signed up for this event, no need to do anything else but delete the event
		if volunteer_ids[0] == '-1':
			event.delete_instance()
			QMessageBox.about(self, " ", "The event has been successfully deleted.")
			return
		del_id = event.get(Event.id == event.id).id
		runtime = self.get_event_runtime(event)
		# for each volunteer at the event
		for uid in volunteer_ids:
			if uid == '':
				break
			uid = int(uid)
			# Get information that needs updating about each user
			user = User.get(User.user_id == uid)
			user_events = user.event_ids
			user_vol_time = user.volunteer_hours

			# remove the event from the users
			u_event_ids = user_events.split(' ')
			u_event_ids.remove(str(del_id))
			u_event_ids = ' '.join(u_event_ids)

			# update the users time
			user_vol_time -= runtime

			# reset the users events to none if they are no longer signed up for any events
			if u_event_ids == '':
				u_event_ids = '-1'

			# Update the User
			User.update({User.event_ids: u_event_ids}).where(User.user_id == uid).execute()
			User.update({User.volunteer_hours: user_vol_time}).where(User.user_id == uid).execute()

		# Delete the event and let the user know
		event.delete_instance()
		QMessageBox.about(self, " ", "The event has been successfully deleted.")
	
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
		
		# set up the help button
		self.help_btn = QPushButton("Help")
		self.help_btn.clicked.connect(self.help_click)
		self.help_btn.setProperty('class', 'normal-bar-btn')
		self.help_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
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
		self.hbox_bar.addWidget(self.about_btn)
		self.hbox_bar.addWidget(self.contact_btn)
		self.hbox_bar.addWidget(self.help_btn)
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
	
	# go to the help page
	def help_click(self):
		self.win.set_page(self.this_page, cs.PAGE_HELP)
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
		
		cs.CURRENT_USER = "Guest"
	
	# go to the login page
	def login_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN)
		self.reset_day()
	
	# go to the new account page
	def signup_click(self):
		self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
		self.reset_day()

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
