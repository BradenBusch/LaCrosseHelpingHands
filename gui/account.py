'''
Account page, all registered users can view their account information here.
Accessibile by: Volunteer, Staff, Administrator

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 04/06/2020

'''

import os
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
		
		# draw the apge
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

		# TODO we can think of splitting the screen after the demo but for now i dont think we need this
		# self.welcome_label = QLabel("My Account")
		# self.welcome_label.setProperty('class', 'cal-label')
		# self.welcome_label.setFixedHeight(62)
		# self.hbox_2.addWidget(self.welcome_label)
		
		# self.user_events_label = QLabel("My Scheduled Events")
		# self.user_events_label.setProperty('class', 'cal-label')
		# self.user_events_label.setFixedHeight(62)
		# self.hbox_2.addWidget(self.user_events_label)
		
		# Divide the screen into halves
		self.vbox_1 = QVBoxLayout()
		# self.vbox_2 = QVBoxLayout()
		
		# set the paragraph of text to display above the picture
		# self.home_desc = QLabel(self.get_text("home_description.txt"))
		# self.home_desc.setProperty('class', 'home-desc-label')
		# self.home_desc.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc)
		
		# self.home_desc1 = QLabel("Welcome to Helping Hands La Crosse!")
		# self.home_desc1.setProperty('class', 'bold-label')
		# self.home_desc1.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc1)
		
		# self.home_desc2 = QLabel(self.get_text("home_description.txt"))
		# self.home_desc2.setProperty('class', 'home-desc-label')
		# self.home_desc2.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc2)
		#
		# self.home_desc3 = QLabel(
		# 	"Interested in volunteering at one of our events and making your mark in the La Crosse community?")
		# self.home_desc3.setProperty('class', 'bold-text-label')
		# self.home_desc3.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc3)
		#
		# self.home_desc4 = QLabel("• Register an account and head over to our Calendar page to register for events!")
		# self.home_desc4.setProperty('class', 'home-desc-label')
		# self.home_desc4.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc4)
		#
		# self.home_desc5 = QLabel("Interested in making a donation to our organization?")
		# self.home_desc5.setProperty('class', 'bold-text-label')
		# self.home_desc5.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc5)
		#
		# self.home_desc6 = QLabel("• Register an account and donate to your heart's content!")
		# self.home_desc6.setProperty('class', 'home-desc-label')
		# self.home_desc6.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc6)
		#
		# self.home_desc7 = QLabel("Interested in joining our staff or administrator team?")
		# self.home_desc7.setProperty('class', 'bold-text-label')
		# self.home_desc7.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc7)
		#
		# self.home_desc8 = QLabel(
		# 	"• Visit the Contact Us page and contact us directly, we'd be delighted to have you join us!")
		# self.home_desc8.setProperty('class', 'home-desc-label')
		# self.home_desc8.setWordWrap(True)
		# self.vbox_1.addWidget(self.home_desc8)
		
		# create labels for the information
		self.events_label = QLabel("My Events")
		self.events_label.setProperty('class', 'home-events-label')
		# self.events_label.setFixedHeight(40)

		# create the my events btn. This necessary because otherwise a database call will be made at __init__
		self.my_events_btn = QPushButton("View My Events")
		self.my_events_btn.setProperty('class', 'special-bar-btn')
		self.my_events_btn.clicked.connect(self.populate_user_events)
		self.my_events = QScrollArea()
		self.vbox_1.addWidget(self.events_label)
		self.vbox_1.addWidget(self.my_events_btn)
		self.vbox_1.addWidget(self.my_events)
		# add two VBoxes to top level HBox
		self.hbox_screen.addLayout(self.vbox_1)
		# self.hbox_screen.addLayout(self.vbox_2)
		
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
		# Build scroll area (its weird, i had to look up so much documentation)
		self.my_events_btn.hide()
		self.my_events_widget = QWidget()
		self.my_events_vbox = QVBoxLayout()
		self.my_events_widget.setLayout(self.my_events_vbox)
		self.my_events.setWidget(self.my_events_widget)
		self.my_events.setWidgetResizable(True)
		# TODO we will change these based on how we want / don't want description
		# self.my_events.setFixedHeight(500)
		# sys_width, sys_height = self.screen_resolution()
		# self.my_events.setFixedWidth((sys_width // 2) - 35)
		self.my_events.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		ids = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		# User is not signed up for any events
		if ids == '-1':
			QMessageBox.about(None, " ", "You aren't currently signed up for any events")
			self.my_events_btn.show()  # Needs to be reshown because the user has no events. This is a weird corner case
			return
		# print(f'cs.CURRENT_USER_ID: {cs.CURRENT_USER_ID}') TODO debug
		event_ids = ids.split(' ')
		for id in event_ids:
			event = Event.get(Event.id == id)
			hbox = QHBoxLayout()
			
			name = QLabel('Name: ')
			name.setProperty('class', 'bold-label')
			hbox.addWidget(name)
			n = QLabel(event.name)
			n.setProperty('class', 'tab-info')
			hbox.addWidget(n)
			
			location = QLabel('Location: ')
			location.setProperty('class', 'bold-label')
			hbox.addWidget(location)
			l = QLabel(event.location)
			l.setProperty('class', 'tab-info')
			hbox.addWidget(l)

			# TODO find some way to format this nicely and make it not ugly
			# description = QLabel('Description: ')
			# description.setProperty('class', 'bold-label')
			# hbox.addWidget(description)
			# d = QLabel(event.description)
			# d.setProperty('class', 'tab-info')
			# hbox.addWidget(d)

			date = QLabel('Date: ')
			date.setProperty('class', 'bold-label')
			hbox.addWidget(date)
			time = '%s/%s/%s, %s-%s' % (event.month, event.day, event.year, event.start_date, event.end_date)
			t = QLabel(time)
			t.setProperty('class', 'tab-info')
			hbox.addWidget(t)

			cancel_btn = QPushButton('Cancel Event')
			cancel_btn.setProperty('class', 'normal-bar-btn')
			cancel_btn.clicked.connect(partial(self.remove_event, event.id))
			hbox.addWidget(cancel_btn)
			self.my_events_vbox.addLayout(hbox)
		# self.vbox_1.addWidget(self.my_events) TODO i think we should delete this

	# delete a volunteering event. This will update the User and Event tables.
	def remove_event(self, event_id):
		# remove the event from the user list
		# print(f'{event_id}')
		user_events = User.get(User.user_id == cs.CURRENT_USER_ID).event_ids
		# print(f'{user_events}s')
		event_ids = user_events.split(' ')
		# print(f'user events {event_ids}')
		event_ids.remove(str(event_id))
		# print(f'user events {event_ids}')
		event_ids = ' '.join(event_ids)
		# print(f'user events {event_ids}s')
		# The user has no events left, so reset it to the value for no events
		if event_ids == '':
			event_ids = '-1'
		# Update the users new events
		User.update({User.event_ids: event_ids}).where(User.user_id == cs.CURRENT_USER_ID).execute()

		# remove the user from the event and decrement the volunteer count
		volunteer_ids = Event.get(Event.id == event_id).volunteers_ids

		# decrement the volunteer count
		volunteer_count = Event.get(Event.id == event_id).volunteers_attending
		volunteer_count -= 1

		# No volunteers, reset the id to -1
		if volunteer_count == 0:
			volunteer_ids = '-1'
		# Else just remove the id from the list
		else:
			volunteer_ids = volunteer_ids.split(' ')
			print(f'volunteers {volunteer_ids}')
			volunteer_ids.remove(str(cs.CURRENT_USER_ID))
			print(f'volunteers {volunteer_ids}')
		# Update the new volunteer count and volunteers
		Event.update({Event.volunteers_attending: volunteer_count}).where(Event.id == event_id).execute()
		Event.update({Event.volunteers_ids: volunteer_ids}).where(Event.id == event_id).execute()
		self.populate_user_events()  # Redraw the scroll area

	# reads in all text from a passed .txt file and returns it as a string
	def get_text(self, filename):
		# if file exists else use the other one (handles path to the image)
		if os.path.isfile('gui\\text\\{}'.format(filename)):
			path = 'gui\\text\\{}'.format(filename)
		else:
			path = 'non_profit\\gui\\text\\{}'.format(filename)
		
		# open the file and read in all text
		with open(path, 'r') as text_file:
			text = text_file.read()
		
		return text
	
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
		self.win.set_page(self.this_page, cs.PAGE_LOGIN)
	
	# go to the new account page
	def signup_click(self):
		self.win.set_page(self.this_page, cs.PAGE_NEW_ACCOUNT)
	
	# TODO add additional button methods here
	
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
	# 	painter = QPainter(self)
	#
	# 	# set the color and pattern of the border of the shape: (color, thickness, pattern)
	# 	painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
	#
	# 	# set the color and pattern of the shape: (r, g, b, alpha)
	# 	painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
	#
	# 	# retrieve the resolution of the system
	# 	sys_width, sys_height = self.screen_resolution()
	#
	# 	# set the properties of the rectangle: (x-coord, y-coord, width, height)
	# 	painter.drawRect(0, 127, sys_width, 60)
	#
	# 	# set the color and pattern of the shape: (r, g, b, alpha)
	# 	painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
	#
	# 	# set the properties of the rectangle: (x-coord, y-coord, width, height)
	# 	painter.drawRect(0, 250, (sys_width // 2) - 5, 675)
	#
	# 	# set the color and pattern of the shape: (r, g, b, alpha)
	# 	painter.setBrush(QBrush(QColor(199, 205, 209, 255), Qt.SolidPattern))
	#
	# 	# set the properties of the rectangle: (x-coord, y-coord, width, height)
	# 	painter.drawRect((sys_width // 2) + 5, 250, (sys_width // 2) - 5, 675)


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
