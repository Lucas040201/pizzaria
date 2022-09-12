from app import app
from flask import render_template, request, flash, redirect

from app.infra.entities.role import Role


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')
