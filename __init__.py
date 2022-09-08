from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})
migrate = Migrate(app, db)

from app.controllers import default
