from app import app
from flask import render_template, request, flash, redirect

from app.infra.entities.role import Role


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    """Home of site"""
    return render_template('index.html', title="Home")
