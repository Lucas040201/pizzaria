from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, csrf

import jwt
import datetime

from app.infra.exceptions.user_exists import UserExists
from app.infra.exceptions.user_not_found import UserNotFound

from app.services.address_service import AddressService
from app.services.user_service import UserService

from app.authenticate import auth_required

user_service = UserService()
address_service = AddressService()


@app.route('/api/login', methods=['POST'])
@csrf.exempt
def login_api():
    """User Login"""
    if not 'password' in request.json or not 'email' in request.json:
        return jsonify({
            "message": "Insira as informacoes de login corretamente"
        }), 400

    email = request.json['email']
    password = request.json['password']

    user = user_service.get_user_by_email(email)

    if user and user.check_login(password):
        token_info = {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }
        token = jwt.encode(token_info, app.config['SECRET_KEY']).decode()
        return jsonify({"token": token})
    else:
        return jsonify({
            "message": "E-mail não encontrado/senha invalida"
        }), 404


@app.route('/api/profile', methods=['GET'])
@csrf.exempt
@auth_required
def profile_api(current_user):
    """User Profile"""
    if not len(current_user.address):
        return jsonify({'error': 'Usuário não possui endereço'}), 400

    payload = user_info(current_user)

    return jsonify({'data': payload})


@app.route('/api/profile', methods=['PUT'])
@csrf.exempt
@auth_required
def profile_update_api(current_user):
    """Update user profile"""
    if not len(current_user.address):
        return jsonify({'error': 'Usuário não possui endereço'}), 400
    try:
        current_user_info = user_info(current_user)

        current_user_new_info = {}
        for index in request.json:
            if index in current_user_info['user']:
                current_user_new_info[index] = request.json[index]

        user_service.update_user(current_user.id, current_user_new_info)

        return jsonify({'message': 'Usuário atualizado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro ao atualizar usuário'})


def user_info(current_user):
    address = current_user.address[0]

    return {
        "user": {
            "name": current_user.name,
            "email": current_user.email,
            "phone": current_user.phone,
            "password": current_user.password,
            "address": {
                "cep": address.cep,
                "street": address.street,
                "district": address.district,
                "number": address.number,
                "uf": address.uf
            }
        }
    }
