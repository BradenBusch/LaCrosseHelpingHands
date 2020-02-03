from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class NewAccount(QWidget):
    def __init__(self):
        super().__init__()
        self.draw()
        self.show()

    def draw(self):
        label = QLabel("BPW")
        label.setAlignment(Qt.AlignCenter)
        self.setWindowTitle("BOP")

    def verify_user(self):
        # Check database, verify the username and password.
        pass