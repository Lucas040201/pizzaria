from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('app.config')
csrf = CSRFProtect(app)

db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

login_manager = LoginManager(app)
migrate = Migrate(app, db)

from app.controllers import default, user, products

