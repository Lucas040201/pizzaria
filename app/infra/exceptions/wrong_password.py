class WrongPassword(Exception):
    def __init__(self, message='Wrong Password'):
        self.message = message
        super().__init__(self.message)
