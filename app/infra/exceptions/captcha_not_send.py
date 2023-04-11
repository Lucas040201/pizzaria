class CaptchaNotSend(Exception):
    def __init__(self, message='Captcha not send'):
        self.message = message
        super().__init__(self.message)
