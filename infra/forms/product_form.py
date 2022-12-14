from wtforms import StringField, PasswordField,\
    SelectField, validators,\
    FloatField
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed

import re

class ProductForm(Form):
    product_name = StringField('Product Name', [validators.DataRequired()])
    price = StringField('Product Price', [validators.DataRequired()])
    description = StringField('Product Description', [validators.DataRequired()])
    excerpt = StringField('Product Excerpt', [validators.DataRequired()])
    image = FileField('Product Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    #                   [
    #
    #     # validators.regexp('([^\\s]+(\\.(?i)(jpe ? g| png | gif | bmp))$)'),
    # ])
    #
    # def validate_image(form, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
