class TooMuchLogin(Exception):
    def __init__(self):
        self.msg = "too much login"

class OutOfTextBox(Exception):
    def __init__(self, size, type):
        self.size = size
        if type is not None:
            self.type = type

class SizeNotFitType2(Exception):
    def __init__(self, size):
        self.size = size