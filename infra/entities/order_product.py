from app import db


class OrderProduct(db.Model):
    __tablename__ = 'orders_products'

    def __init(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order = db.relationship('Order', backref=db.backref('orders_products'), lazy='subquery')
    product = db.relationship('Product', backref=db.backref('orders_products'), lazy='subquery')
