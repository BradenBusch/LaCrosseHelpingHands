'''
Account page, all registered users can view their account information here.

Accessible by: Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/22/2020

'''

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


class Account(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# set window title and properties, initialize the window reference
		self.setProperty('class', 'homepage')
		self.setWindowTitle('My Account')
		self.win = None
		self.this_page = cs.PAGE_ACCOUNT
		
		# restricts user input to integers only
		self.onlyInt = QIntValidator()
		
		# draw the page
		self.draw()
	
	# adds all buttons and sets up the layout
	def draw(self):
		self.vbox_screen = QVBoxLayout()
		
		self.hbox_1 = QHBoxLayout()
		self.spacer_1 = QLabel("")
		self.spacer_1.setProperty('class', 'acc-bar-spacer-label')
		self.hbox_1.addWidget(self.spacer_1)
		self.vbox_screen.addLayout(self.hbox_1)
		
		# create the top bar of tabs for the application
		self.top_bar()
		
		# create HBoxes
		self.hbox_2 = QHBoxLayout()
		self.hbox_screen = QHBoxLayout()
		
		self.account_label = QLabel("My Account")
		self.account_label.setProperty('class', 'cal-label')
		self.account_label.setFixedHeight(62)
		self.hbox_2.addWidget(self.account_label)
		
		# Divide the screen into halves
		self.vbox_1 = QVBoxLayout()
		self.vbox_2 = QVBoxLayout()
		
		# set the account information
		self.acc_desc_1 = QLabel("Account Information")
		self.acc_desc_1.setProperty('class', 'bold-under-label')
		self.vbox_1.addWidget(self.acc_desc_1)
		
		# set the account type
		self.acc_desc_2 = QLabel("Account Type:")
		self.acc_desc_2.setProperty('class', 'acc-bold-text-label')
		self.hbox_4 = QHBoxLayout()
		self.acc_type = QLabel("Guest")
		self.acc_type.setProperty('class', 'acc-desc-label')
		self.hbox_4.addWidget(self.acc_desc_2)
		self.hbox_4.addWidget(self.acc_type)
		self.vbox_1.addLayout(self.hbox_4)
		
		# set the username
		self.acc_desc_3 = QLabel("Username:")
		self.acc_desc_3.setProperty('class', 'acc-bold-text-label')
		self.hbox_5 = QHBoxLayout()
		self.acc_name = QLabel("Username")
		self.acc_name.setProperty('class', 'acc-desc-label')
		self.hbox_5.addWidget(self.acc_desc_3)
		self.hbox_5.addWidget(self.acc_name)
		self.vbox_1.addLayout(self.hbox_5)
		
		# set the email
		self.acc_desc_4 = QLabel("E-Mail:")
		self.acc_desc_4.setProperty('class', 'acc-bold-text-label')
		self.hbox_6 = QHBoxLayout()
		self.acc_email = QLabel("E-Mail")
		self.acc_email.setProperty('class', 'acc-desc-label')
		self.hbox_6.addWidget(self.acc_desc_4)
		self.hbox_6.addWidget(self.acc_email)
		self.vbox_1.addLayout(self.hbox_6)
		
		# set the account statistics
		self.acc_desc_5 = QLabel("Account Statistics")
		self.acc_desc_5.setProperty('class', 'bold-under-label')
		self.vbox_1.addWidget(self.acc_desc_5)
		
		# set the total number of hours volunteered
		self.acc_desc_6 = QLabel("Total Hours Volunteered:           ")
		self.acc_desc_6.setProperty('class', 'acc-bold-text-label')
		self.hbox_7 = QHBoxLayout()
		self.acc_hours = QLabel("Hours")
		self.acc_hours.setProperty('class', 'acc-desc-label')
		self.hbox_7.addWidget(self.acc_desc_6)
		self.hbox_7.addWidget(self.acc_hours)
		self.vbox_1.addLayout(self.hbox_7)
		
		# set the total amount of money donated
		self.acc_desc_7 = QLabel("Total Monetary Donations:      $")
		self.acc_desc_7.setProperty('class', 'acc-bold-text-label')
		self.hbox_8 = QHBoxLayout()
		self.acc_money = QLabel("Money")
		self.acc_money.setProperty('class', 'acc-desc-label')
		self.hbox_8.addWidget(self.acc_desc_7)
		self.hbox_8.addWidget(self.acc_money)
		self.vbox_1.addLayout(self.hbox_8)
		
		# HBox to hold buttons
		self.hbox_btn = QHBoxLayout()
		
		# spacer button
		self.spacer_btn = QLabel("                 ")
		
		# create the organization donate button
		self.org_don_btn = QPushButton('Donate to Organization')
		self.org_don_btn.setProperty('class', 'long-bar-btn')
		self.org_don_btn.clicked.connect(partial(self.create_donation_form, cs.ORG_ID, "Organization Donation"))
		self.org_don_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# create the generate reports button
		self.admin_priv_btn = QPushButton('Administrator Privileges')
		self.admin_priv_btn.setProperty('class', 'long-bar-btn')
		self.admin_priv_btn.clicked.connect(self.admin_privileges)
		self.admin_priv_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# add the buttons to the layout
		self.hbox_btn.addWidget(self.spacer_btn)
		self.hbox_btn.addWidget(self.org_don_btn)
		self.hbox_btn.addWidget(self.admin_priv_btn)
		self.hbox_btn.setAlignment(Qt.AlignCenter)
		self.vbox_1.addLayout(self.hbox_btn)
		self.vbox_1.setAlignment(Qt.AlignLeft)
		
		# create labels for the information
		self.events_label = QLabel("My Events")
		self.events_label.setProperty('class', 'home-events-label')
		self.events_label.setFixedHeight(40)
		self.events_label.setAlignment(Qt.AlignCenter)
		self.vbox_2.addWidget(self.events_label)
		
		# populate the scroll area with the user's upcoming events
		self.populate_user_events()
		# add two VBoxes to top level HBox
		self.hbox_screen.addLayout(self.vbox_1)
		self.hbox_screen.addLayout(self.vbox_2)
		
		# add HBoxes to top level VBox
		self.vbox_screen.addLayout(self.hbox_2)
		self.vbox_screen.addLayout(self.hbox_screen)
		
		# create spacer for bottom of screen
		self.hbox_3 = QHBoxLayout()
		self.spacer_2 = QLabel("")
		self.spacer_2.setProperty('class', 'acc-bottom-spacer-label')
		self.hbox_3.addWidget(self.spacer_2)
		self.vbox_screen.addLayout(self.hbox_3)
		
		# set up the layout
		self.setLayout(self.vbox_screen)
		
		# set the geometry of the window
		sys_width, sys_height = self.screen_resolution()
		self.x_coord = 0
		self.y_coord = 40
		self.width = sys_width
		self.height = sys_height
		self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)
	
	# populate the user's events
	def populate_user_events(self):
		# hide the donation tabs, if it exists
		try:
			self.tabs.hide()
		except:
			pass
		
		# Build the scroll area
		self.my_events_widget = QWidget()
		self.my_events_vbox = QVBoxLayout()
		self.my_events_widget.setLayout(self.my_events_vbox)
		self.my_events = QScrollArea()
		self.my_events.setWidget(self.my_events_widget)
		self.my_events.setWidgetResizable(True)
		self.my_events.setFixedHeight(575)
		sys_width, sys_height = self.screen_resolution()
		self.my_events.setFixedWidth((2 * sys_width // 3) - 35)
		self.my_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		try:
			ids = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		except:
			ids = "-1"
		
		# if the user is not signed up for any events
		if ids == '-1':
			hbox = QHBoxLayout()
			no_events = QLabel('You are not registered for any events!')
			no_events.setAlignment(Qt.AlignCenter)
			no_events.setProperty('class', 'no-events-label')
			hbox.addWidget(no_events)
			self.my_events_vbox.addLayout(hbox)
			self.vbox_2.addWidget(self.my_events)
			return
		
		# holds event ids from database
		event_ids = ids.split(' ')
		
		# master list to hold all events
		master_events = []
		
		# build up all event data
		for id in event_ids:
			event = Event.get(Event.id == id)
			
			# retrieve all relevant information
			master_events.append([event.name,
								  event.location,
								  event.month,
								  event.day,
								  event.year,
								  event.start_date,
								  event.end_date,
								  id])
		
		# set the current date and time
		self.currentMonth = datetime.now().month
		self.currentYear = datetime.now().year
		self.currentDay = datetime.now().day
		
		# filter out events that have already passed and sort the events by date
		master_events = [event for event in master_events if not int(event[4]) < self.currentYear]
		master_events = [event for event in master_events if not ((int(event[2]) < self.currentMonth) and
																  (int(event[4]) <= self.currentYear))]
		master_events = [event for event in master_events if not ((int(event[3]) < self.currentDay) and
																  (int(event[2]) <= self.currentMonth))]
		master_events.sort(key=lambda x: (int(x[4]), int(x[2]), int(x[3]), x[5]))
		
		# if there are no events the user has signed up for
		if len(master_events) == 0:
			# inform the user that no events have been scheduled yet
			hbox = QHBoxLayout()
			no_events = QLabel('You are not registered for any events!')
			no_events.setAlignment(Qt.AlignCenter)
			no_events.setProperty('class', 'no-events-label')
			hbox.addWidget(no_events)
			self.my_events_vbox.addLayout(hbox)
			self.vbox_2.addWidget(self.my_events)
			return
		
		# fill in the user's upcoming events
		for event in master_events:
			hbox = QHBoxLayout()
			
			# fill in the event name
			name = QLabel('Name:')
			name.setProperty('class', 'bold-label')
			hbox.addWidget(name)
			n = QLabel(event[0])
			n.setProperty('class', 'tab-info')
			hbox.addWidget(n)
			
			# fill in the event location
			location = QLabel('Location:')
			location.setProperty('class', 'bold-label')
			hbox.addWidget(location)
			l = QLabel(event[1])
			l.setProperty('class', 'tab-info')
			hbox.addWidget(l)
			
			# fill in the event date
			date = QLabel('Date:')
			date.setProperty('class', 'bold-label')
			hbox.addWidget(date)
			time = '%s/%s/%s, %s-%s' % (event[2], event[3], event[4], event[5], event[6])
			t = QLabel(time)
			t.setProperty('class', 'tab-info')
			hbox.addWidget(t)
			
			# create the donate button
			donate_btn = QPushButton('Donate')
			donate_btn.setProperty('class', 'normal-bar-btn')
			donate_btn.clicked.connect(partial(self.create_donation_form, event[7], "Event Donation"))
			donate_btn.setCursor(QCursor(Qt.PointingHandCursor))
			
			# create the cancel event button
			cancel_btn = QPushButton('Cancel Registration')
			cancel_btn.setProperty('class', 'red-bar-btn')
			cancel_btn.clicked.connect(partial(self.remove_event, event[7]))
			cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
			
			# add the buttons to the HBox
			hbox.addWidget(donate_btn)
			hbox.addWidget(cancel_btn)
			
			# set up the layouts
			hbox_2 = QHBoxLayout()
			spacer = QLabel("")
			spacer.setProperty('class', 'upcoming-label')
			hbox_2.addWidget(spacer)
			
			self.my_events_vbox.addLayout(hbox)
			self.my_events_vbox.addLayout(hbox_2)
		
		# add the scroll area to the VBox
		self.vbox_2.addWidget(self.my_events)
	
	# hides the previous items from view
	def hide_previous(self):
		# hide the scrollbox
		self.my_events.hide()
	
	# creates the donation form so the user can donate
	def create_donation_form(self, event_id, title):
		self.hide_previous()
		# attempt to hide the tabs if they are already open
		try:
			self.tabs.hide()
		except:
			pass
		
		# set up the tabs
		self.tabs = QTabWidget()
		self.tabs.setProperty('class', 'tab-layout')
		self.tabs.setFixedHeight(575)
		sys_width, sys_height = self.screen_resolution()
		self.tabs.setFixedWidth((2 * sys_width // 3) - 35)
		self.vbox_2.addWidget(self.tabs)
		
		# remove all tabs
		for i in range(self.tabs.count()):
			self.tabs.removeTab(0)
		
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
		cancel_btn.clicked.connect(partial(self.populate_user_events))
		cancel_btn.setProperty('class', 'red-bar-btn')
		cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		confirm_btn = QPushButton("Confirm")
		# If donating to event(not organization)
		if title != "Organization Donation":
			confirm_btn.clicked.connect(partial(self.verify_donation, donation_field, event_id))
		# If donating to the organization
		else:
			confirm_btn.clicked.connect(partial(self.verify_org_donation, donation_field))
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
		self.tabs.addTab(form, title)
	
	# verify that the donation is valid and update the event and users donations
	def verify_donation(self, amount, event_id=None):
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
		self.populate_user_events()
		self.set_account_info()

	# verify that the donation is valid and update the OrgEvent and users donations
	def verify_org_donation(self, amount):
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
			curr_donation = OrgEvent.get(OrgEvent.id == cs.ORG_ID).donations
			user_donations = User.get(User.user_id == cs.CURRENT_USER_ID).total_donations
			curr_donation = curr_donation + int(amount.text())
			user_donations = user_donations + int(amount.text())
			OrgEvent.update(donations=curr_donation).where(OrgEvent.id == cs.ORG_ID).execute()
			User.update(total_donations=user_donations).where(User.user_id == cs.CURRENT_USER_ID).execute()
			QMessageBox.about(self, " ", "Thank you for the donation!")
		self.populate_user_events()
		self.set_account_info()
		print(f'total donations for OrgEvent {curr_donation}') # TODO comment this out
	
	# Decrement the users volunteer hours when they cancel an event
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
		total_hours = float(user_time) - float(event_hours)
		User.update({User.volunteer_hours: total_hours}).where(User.user_id == cs.CURRENT_USER_ID).execute()
	
	# un-volunteer from a volunteering event. This will update the User and Event tables.
	def remove_event(self, event_id):
		# remove the event from the user list
		user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		event_ids = user_events.split(' ')
		event_ids.remove(str(event_id))
		event_ids = ' '.join(event_ids)

		# Update users volunteer hours
		s_time = Event.get(Event.id == event_id).start_date
		e_time = Event.get(Event.id == event_id).end_date
		self.update_user_volunteer_hours(s_time, e_time)

		# The user has no events left, so reset it to the value for no events
		if event_ids == '':
			event_ids = '-1'
		# Update the users new events. Remove the user from the event and decrement the volunteer count
		User.update({User.event_ids: event_ids}).where(User.user_id == cs.CURRENT_USER_ID).execute()
		volunteer_ids = Event.get(Event.id == event_id).volunteers_ids
		volunteer_count = Event.get(Event.id == event_id).volunteers_attending
		volunteer_count -= 1
		# No volunteers, reset the id to -1
		if volunteer_count == 0:
			volunteer_ids = '-1'
		# Remove the id of the current active user
		else:
			volunteer_ids = volunteer_ids.split(' ')
			volunteer_ids.remove(str(cs.CURRENT_USER_ID))
			volunteer_ids = ' '.join(volunteer_ids)
		# Update the new volunteer count and volunteers
		# print(f'volunteer when updating {volunteer_ids} num {volunteer_count}')
		Event.update({Event.volunteers_attending: volunteer_count}).where(Event.id == event_id).execute()
		Event.update({Event.volunteers_ids: volunteer_ids}).where(Event.id == event_id).execute()
		QMessageBox.warning(self, " ", "You are now un-registered from this event.\n\n" + \
									   "Any monetary donations you made to this event will remain donated.\n" + \
									   "If you would like to have this money refunded, please contact us " + \
									   "via our Contact Us page!")
		self.hide_previous()    # get rid of previous scroll area
		self.populate_user_events()    # Redraw the scroll area
		self.set_account_info()    # update the account information
	
	# check if the account is an administrator account
	def check_account(self):
		# hide previous buttons
		self.spacer_btn.hide()
		self.org_don_btn.hide()
		self.admin_priv_btn.hide()
		
		# recreate the organization donate button
		self.org_don_btn = QPushButton('Donate to Organization')
		self.org_don_btn.setProperty('class', 'long-bar-btn')
		self.org_don_btn.clicked.connect(partial(self.create_donation_form, cs.ORG_ID, "Organization Donation"))
		self.org_don_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# recreate the generate reports button
		self.admin_priv_btn = QPushButton('Administrator Privileges')
		self.admin_priv_btn.setProperty('class', 'long-bar-btn')
		self.admin_priv_btn.clicked.connect(self.admin_privileges)
		self.admin_priv_btn.setCursor(QCursor(Qt.PointingHandCursor))
		
		# determine the size of the spacer button
		if cs.CURRENT_USER == "Administrator":
			self.spacer_btn = QLabel("                                  ")
			self.admin_priv_btn.show()
		else:
			self.spacer_btn = QLabel("                                                                    ")
			self.admin_priv_btn.hide()
		
		# re-add the buttons to the layout
		self.hbox_btn.addWidget(self.spacer_btn)
		self.hbox_btn.addWidget(self.org_don_btn)
		self.hbox_btn.addWidget(self.admin_priv_btn)
	
	# updates the QLabels associated with account information
	def set_account_info(self):
		# retrieve user from the database
		user = User.get(User.user_id == cs.CURRENT_USER_ID)
		
		# set the account type
		self.acc_type.setText("{}".format(user.account_type))
		
		# set the username
		self.acc_name.setText("{}".format(user.username))
		
		# set the email
		self.acc_email.setText("{}".format(user.account_email))
		
		# set the total number of hours volunteered
		self.acc_hours.setText("{}".format(user.volunteer_hours))
		
		# set the total amount of money donated
		self.acc_money.setText("{}".format(user.total_donations))
	
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
	
	# go to the calendar page
	def cal_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CAL)
	
	# go to the about us page
	def about_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ABOUT)
	
	# go to the contact us page
	def contact_click(self):
		self.win.set_page(self.this_page, cs.PAGE_CONTACT)
	
	# go to the help page
	def help_click(self):
		self.win.set_page(self.this_page, cs.PAGE_HELP)
	
	# go to the search page
	def search_click(self):
		self.win.set_page(self.this_page, cs.PAGE_SEARCH)
	
	# go to the account page
	def account_click(self):
		self.win.set_page(self.this_page, cs.PAGE_ACCOUNT)
	
	# return to the login signup screen
	def logout_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN_SIGNUP)
		
		cs.CURRENT_USER = "Guest"
	
	# go to the login page
	def login_click(self):
		self.win.set_page(self.this_page, cs.PAGE_LOGIN)
	
	# go to the new account page
	def signup_click(self):
		self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
	
	# go to the administrator priveleges page
	def admin_privileges(self):
		self.win.set_page(self.this_page, cs.PAGE_PRIVILEGES)
	
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
		
		# set the color and pattern of the shape: (r, g, b, alpha)
		painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
		
		# set the properties of the rectangle: (x-coord, y-coord, width, height)
		painter.drawRect(0, 250, (sys_width // 3) - 5, 675)
		
		# set the color and pattern of the shape: (r, g, b, alpha)
		painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
		
		# set the properties of the rectangle: (x-coord, y-coord, width, height)
		painter.drawRect((sys_width // 3) + 5, 250, (2 * sys_width // 3) - 5, 675)
	
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
