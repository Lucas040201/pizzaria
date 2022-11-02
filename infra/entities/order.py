from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    def __init(self, user_id, order_date):
        self.user_id = user_id
        self.order_date = order_date


    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    order_products = db.relationship('OrderProduct', backref=db.backref('orders'), lazy='subquery')