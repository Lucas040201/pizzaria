import os
from functools import wraps

from flask import Flask, Blueprint, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

app = Flask(__name__)
app.config.from_object('app.config')
csrf = CSRFProtect(app)

db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', default="")
GOOGLE_CLIENT_SECRET = os.getenv('GOOLE_SECRET_KEY', default="")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def is_admin(func):
    """Verify if current user is an admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

from app.controllers import default, user, products, payment, order
from app.controllers.api import user

