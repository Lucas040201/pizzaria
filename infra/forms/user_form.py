from wtforms import Form, StringField, PasswordField, SelectField, validators

class UserForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    cep = StringField('CEP', [validators.DataRequired()])
    district = StringField('District', [validators.DataRequired()])
    street = StringField('Street', [validators.DataRequired()])
    number = StringField('Number', [validators.DataRequired()])
    uf = SelectField('UF', [validators.DataRequired()])




