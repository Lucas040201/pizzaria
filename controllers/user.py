from app import app
from flask import render_template, request, flash, redirect, url_for

from app.infra.exceptions.user_exists import UserExists
from app.services.address_service import AddressService
from app.services.user_service import UserService
from app.infra.forms.login_form import LoginForm
from app.infra.forms.user_form import UserForm

user_service = UserService()
address_service = AddressService()


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login-action', methods=['POST'])
def login_action():
    form_submited = request.form
    form = LoginForm(form_submited)
    if form.validate():
        return """RECEBA"""


@app.route('/inscrever-se', methods=['GET'])
def signup():
    form = UserForm()
    return render_template('signup.html', form=form)


@app.route('/cadastrar-action', methods=['POST'])
def signup_action():
    try:
        request_form = request.form
        form = UserForm(request_form)
        print(form.errors)
        if form.validate():
            user = user_service.insert_user(request_form)
            address_service.insert_address(user, request_form)

            return redirect('/listar-usuarios')
        return redirect(url_for('signup'))
    except UserExists as e:
        flash('Usuário já existe')
        return redirect('/inscrever-se')

    except Exception as e:
        print(e)
        flash('Erro ao cadastrar um novo usuário')
        return redirect('/inscrever-se')


@app.route('/listar-usuarios', methods=['GET'])
def list_users():
    users = user_service.list()
    return render_template('list-users.html', users=users)


@app.route('/excluir-usuario/<user_id>', methods=['GET'])
def delete_user(user_id):
    user, address = user_service.select_user_with_address(user_id)
    address_service.delete(address.id)
    user_service.delete(user.id)
    return redirect('/listar-usuarios')


@app.route('/editar-usuario/<user_id>', methods=['GET'])
def edit_user(user_id):
    user, address = user_service.select_user_with_address(user_id)
    return render_template('signup.html', user=user, address=address)


@app.route('/editar-usuario-action/<user_id>', methods=['POST'])
def edit_user_action(user_id):
    try:
        request_form = request.form
        form = UserForm(request_form)
        if form.validate():
            address_id = form['address_id']
            user_service.update_user(user_id, form)
            address_service.update_address(address_id, form)
            return redirect(f"/editar-usuarios/{user_id}")
    except Exception as e:
        flash('Erro ao atualizar usuário')
        return redirect('/listar-usuarios')
