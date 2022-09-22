from wtforms import Form, StringField, PasswordField, SelectField, validators


class UserFormRegister(Form):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    cep = StringField('CEP', [validators.DataRequired()])
    district = StringField('District', [validators.DataRequired()])
    street = StringField('Street', [validators.DataRequired()])
    number = StringField('Number', [validators.DataRequired()])
    uf = SelectField('UF',
                     [validators.DataRequired()],
                     choices=[
                         ('', 'Estados'),
                         ('AC', 'Acre'),
                         ('AL', 'Alagoas'),
                         ('AP', 'Amapá'),
                         ('AM', 'Amazonas'),
                         ('BA', 'Bahia'),
                         ('CE', 'Ceará'),
                         ('DF', 'Distrito Federal'),
                         ('ES', 'Espirito Santo'),
                         ('GO', 'Goiás'),
                         ('MA', 'Maranhão'),
                         ('MS', 'Mato Grosso do Sul'),
                         ('MT', 'Mato Grosso'),
                         ('MG', 'Minas Gerais'),
                         ('PA', 'Pará'),
                         ('PB', 'Paraíba'),
                         ('PR', 'Paraná'),
                         ('PE', 'Pernambuco'),
                         ('PI', 'Piauí'),
                         ('RJ', 'Rio de Janeiro'),
                         ('RN', 'Rio Grande do Norte'),
                         ('RS', 'Rio Grande do Sul'),
                         ('RO', 'Rondônia'),
                         ('RR', 'Roraima'),
                         ('SC', 'Santa Catarina'),
                         ('SP', 'São Paulo'),
                         ('SE', 'Sergipe'),
                         ('TO', 'Tocantins')
                     ])
