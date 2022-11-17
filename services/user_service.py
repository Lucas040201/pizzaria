from flask_login import login_user
from app.infra.exceptions.user_not_found import UserNotFound
from app.infra.repository.user_repository import UserRepository
from app.services.service_base import ServiceBase
from app.infra.exceptions.user_exists import UserExists
from app.infra.entities.user import User
from app.infra.entities.address import Address
from app.infra.forms.login_form import LoginForm
from werkzeug.security import generate_password_hash
import bcrypt

from app.infra.exceptions.user_exists import UserExists
from app.infra.exceptions.user_not_found import UserNotFound
from app.infra.exceptions.wrong_password import WrongPassword
from app.infra.exceptions.invalid_form import InvalidForm
from app.infra.exceptions.captcha_not_send import CaptchaNotSend
from app.infra.exceptions.invalid_captcha import InvalidCaptcha

from app.services.google_service import GoogleService


class UserService(ServiceBase):
    _google_service: GoogleService

    def __init__(self):
        super(UserService, self).__init__(UserRepository())
        self.__google_service = GoogleService()

    def insert_user(self, data: {}) -> User:

        user = self.repository().get_user_by_email(data['email'])

        if user:
            raise UserExists()

        role_id = 2
        if 'role_id' in data:
            role_id = data['role_id']

        new_user = {
            "name": data['name'],
            "password": generate_password_hash(data['password']),
            "email": data['email'],
            "phone": data['phone'],
            "role_id": role_id,
        }

        stored_user = self.insert(new_user)
        return stored_user

    def get_user_with_address(self, user_id: int) -> {User, Address}:
        items = self.repository().get_user_with_address(user_id)
        if not items:
            raise UserNotFound()

        user = items[0]
        address = items[1]
        return user, address

    def update_user(self, user_id: int, data: {}):
        user = self.show(user_id)
        print('atualizando')
        if not user:
            raise UserNotFound()

        user_info = {
            "name": None,
            "email": None,
            "phone": None,
            "password": None
        }
        new_user_info = {}
        for x in data:
            if data[x] and x in user_info:
                if x == 'password':
                    new_user_info[x] = generate_password_hash(data[x])
                else:
                    new_user_info[x] = data[x]

        print(new_user_info)

        updated_user = self.update(user_id, new_user_info)
        return updated_user

    def get_user_by_email(self, email: str) -> User:
        return self.repository().get_user_by_email(email)

    def make_login(self, form_data: []):
        form = LoginForm(form_data)

        if not form.validate():
            raise InvalidForm('Formulário invalido, preencha os campos corretamente')

        if not form_data['g-recaptcha-response']:
            raise CaptchaNotSend('Por favor, selecione a caixa abaixo')

        if not self.__google_service.make_recaptcha_request(form_data['g-recaptcha-response']):
            raise InvalidCaptcha('Captcha invalido. Por favor, marque a caixa abaixo')

        user = self.get_user_by_email(form_data['email'])

        if not user:
            raise UserNotFound('Usuário não encontrado e/ou senha invalida')

        if not user.check_login(form_data['password']):
            raise WrongPassword('Usuário não encontrado e/ou senha invalida')

        login_user(user)


    def google_redirect(self):
        return self.__google_service.get_google_redirect_uri()

    def make_google_login(self):
        response = self.__google_service.get_google_user()
        if response.json().get("email_verified"):
            users_email = response.json()["email"]
            users_name = response.json()["given_name"]

            user = self.get_user_by_email(users_email)

            if user:
                login_user(user)
            else:
                data = {
                    'name': users_name,
                    'email': users_email,
                    'password': '123',
                    'phone': None
                }
                user = self.insert_user(data)
                login_user(user)