from app.infra.entities.address import Address
from app.infra.entities.user import User
from app.infra.repository.repository_base import RepositoryBase


class UserRepository(RepositoryBase):

    def __init__(self):
        super(UserRepository, self).__init__(User)

    def get_user_by_email(self, email):
        with self.create_handler() as db:
            data = db.session.query(User).filter(User.email == email).first()
            return data

    def get_user_with_address(self, user_id):
        with self.create_handler() as db:
            data = db.session.query(User) \
                .join(Address, Address.user_id == User.id) \
                .with_entities(User, Address) \
                .filter(User.id == user_id) \
                .first()
            return data
