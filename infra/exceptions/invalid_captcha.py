class InvalidCaptcha(Exception):
    def __init__(self, message='Invalid Form'):
        self.message = message
        super().__init__(self.message)
