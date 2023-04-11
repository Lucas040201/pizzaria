from wtforms import Form, StringField, PasswordField, SelectField


class UserFormUpdate(Form):
    name = StringField('Name', [])
    email = StringField('Email Address', [])
    password = PasswordField('Password', [])
    phone = StringField('Phone', [])
    cep = StringField('CEP', [])
    district = StringField('District', [])
    street = StringField('Street', [])
    number = StringField('Number', [])
    uf = SelectField('UF',
                     [],
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