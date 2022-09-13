from app.infra.exceptions.user_not_found import UserNotFound
from app.infra.repository.user_repository import UserRepository
from app.services.service_base import ServiceBase
from app.infra.exceptions.user_exists import UserExists
from app.infra.entities.user import User
from app.infra.entities.address import Address
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt


class UserService(ServiceBase):
    def __init__(self):
        super(UserService, self).__init__(UserRepository())

    def insert_user(self, data: []) -> User:

        user = self.repository().get_user_by_email(data['email'])

        if user:
            raise UserExists()

        password = generate_password_hash(data['password'])

        role_id = 2
        if 'role_id' in data:
            role_id = data['role_id']

        new_user = {
            "name": data['name'],
            "password": password,
            "email": data['email'],
            "phone": data['phone'],
            "role_id": role_id,
        }

        stored_user = self.insert(new_user)
        return stored_user

    def get_user_with_address(self, user_id: int) -> {User, Address}:
        items = self.repository().get_user_with_address(user_id)
        if not items:
            raise Exception

        user = items[0]
        address = items[1]
        return user, address

    def update_user(self, user_id: int, data: []):
        user = self.show(user_id)

        if not user:
            raise UserNotFound()

        user_info = {
            "name": data['name'],
            "email": data['email'],
            "phone": data['phone'],
        }

        if 'password' in data:
            user_info['password'], user_info['salt'] = self.__generate_password(data['password'])

        updated_user = self.update(user_id, user_info)

        return updated_user

    def __generate_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        password = password.encode('utf8')
        password = bcrypt.hashpw(password, salt)
        return password, salt

    def get_user_by_email(self, email: str) -> User:
        return self.repository().get_user_by_email(email)

    def check_login(self, user: User, password: str) -> bool:
        return check_password_hash(user.password, password)

