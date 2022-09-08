from app import db


class User(db.Model):
    __tablename__ = 'users'

    def __init(self, name, password, email, phone, role_id=2, salt=None):
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.role_id = role_id
        if salt:
            self.salt = salt

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    salt = db.Column(db.String)
    address = db.relationship('Address', backref=db.backref('users'), lazy='subquery')

    def __repr__(self):
        return f"[User name={self.name} email={self.email}]"
