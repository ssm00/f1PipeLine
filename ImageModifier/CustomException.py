class TooMuchLogin(Exception):
    def __init__(self):
        self.msg = "too much login"

class OutOfTextBox(Exception):
    def __init__(self, size):
        self.size = size
