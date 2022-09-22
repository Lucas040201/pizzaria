from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app.services.user_service import UserService

user_service = UserService()

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({"error": "Você não tem permissão para acessar essa rota"}), 403

        if not "Bearer" in token:

            return jsonify({"error": "token invalido."}), 401

        try:
            token_pure = token.replace("Bearer ", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = user_service.show(decoded['id'])
        except Exception as e:
            return jsonify({"error": "O token é invalido."}), 403

        return func(current_user=current_user, *args, **kwargs)
    return wrapper