from wtforms import Form, BooleanField, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])