from app import db


class Product(db.Model):
    __tablename__ = 'products'

    def __init__(self, product_name, price, description, excerpt, image):
        self.product_name = product_name
        self.price = price
        self.description = description
        self.excerpt = excerpt
        self.image = image

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    excerpt = db.Column(db.String)
    image = db.Column(db.String)

    def __repr__(self):
        return f"Product product_name={self.product_name}"
