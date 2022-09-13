from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    def __init(self, name, password, email, phone, role_id=2):
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.role_id = role_id

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    address = db.relationship('Address', backref=db.backref('users'), lazy='subquery')

    def __repr__(self):
        return f"[User name={self.name} email={self.email}]"
