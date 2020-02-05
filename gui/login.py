from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Login(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QLabel("BPW")
        # label.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('How are you?')
        self.windowTitle()

    # Check database, verify the username and password.
    def verify_user(self):
        pass
