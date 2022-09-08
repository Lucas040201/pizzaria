class UserExists(Exception):
    def __init__(self, message='user already registered'):
        self.message = message
        super().__init__(self.message)
