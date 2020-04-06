'''

'''

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
try:
	from non_profit.models.database import *
	from non_profit import constants as cs
except:
	from models.database import *
	import constants as cs


class Account(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Account')
		self.win = None

		self.this_page = cs.PAGE_ACCOUNT

		self.draw()

	def draw(self):
		self.vbox_screen = QVBoxLayout()

		self.my_events_label = QLabel('My Events')
		self.my_events_label.setProperty('class', 'home-events-label')
		self.vbox_screen.addWidget(self.my_events_label)

		# set the overall layout
		self.setLayout(self.vbox_screen)  # TODO set layout according to the layout chosen

		# set the geometry of the window    # TODO set geometry of the window correctly
		sys_width, sys_height = self.screen_resolution()
		self.x_coord = 0
		self.y_coord = 40
		self.width = sys_width
		self.height = sys_height
		self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)

	# returns the resolution of the current system (width and height)
	def screen_resolution(self):
		# retrieve the resolution of the current system
		geometry = QDesktopWidget().screenGeometry(0)

		return geometry.width(), geometry.height()
