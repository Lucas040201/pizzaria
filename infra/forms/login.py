from wtforms import Form, BooleanField, StringField, PasswordField, validators

class Login(Form):
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])