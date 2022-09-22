from app import db

class Address(db.Model):

    def __init__(self, user_id, cep, number, district, street, uf):
        self.user_id = user_id
        self.cep = cep
        self.number = number
        self.district = district
        self.street = street
        self.uf = uf

    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cep = db.Column(db.String)
    number = db.Column(db.String)
    district = db.Column(db.String)
    street = db.Column(db.String)
    uf = db.Column(db.String)

    def __repr__(self):
        return f"Address cep={self.cep}, street={self.street}"

