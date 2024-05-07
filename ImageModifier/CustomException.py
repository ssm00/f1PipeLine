class TooMuchLogin(Exception):
    def __init__(self):
        self.msg = "too much login"