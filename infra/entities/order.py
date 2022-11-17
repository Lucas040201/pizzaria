from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    order_products = db.relationship('OrderProduct', backref=db.backref('orders'), lazy='subquery')
    user = db.relationship('User', backref=db.backref('orders'), lazy='subquery')

    def __init(self, user_id, order_date):
        self.user_id = user_id
        self.order_date = order_date

    def get_amount(self):
        amount = 0
        for product in self.order_products:
            amount += product.price

        return amount