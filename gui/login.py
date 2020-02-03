from PyQt5.QtWidgets import QApplication, QWidget
import random
import uuid


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.draw()
        print(self.generate_id())

    def draw(self):
        pass

    # Store the new users information in the database
    def store_user(self):
        user_id = self.generate_id()

    # Generate a unique ID for each user in the database
    def generate_id(self):
        # return uuid.uuid4().hex[:4]
        digits = set(range(10))
        first = random.randint(1, 9)
        last_3 = random.sample(digits - {first}, 3)
        return str(first) + ''.join(map(str, last_3))
