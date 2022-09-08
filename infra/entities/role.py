from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String())
    users = db.relationship("User", backref=db.backref('users', lazy='subquery'))
