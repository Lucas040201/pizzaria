from app import db


class Product(db.Model):

    def __init__(self, product_name, price, description, image):
        self.product_name = product_name
        self.price = price
        self.description = description
        self.image = image

    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    image = db.Column(db.String)


    def __repr__(self):
        return f"Product product_name={self.product_name}"

