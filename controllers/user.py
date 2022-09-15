from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, is_admin

from app.infra.exceptions.user_exists import UserExists
from app.infra.exceptions.user_not_found import UserNotFound

from app.services.address_service import AddressService
from app.services.user_service import UserService

from app.infra.forms.login_form import LoginForm
from app.infra.forms.user_form import UserForm

user_service = UserService()
address_service = AddressService()


@app.route('/login', methods=['GET'])
def login():
    """Login view"""
    form = LoginForm()
    return render_template('login.html', form=form, title="Fazer Login")


@app.route('/login-action', methods=['POST'])
def login_action():
    """Action for user login"""
    form_submited = request.form
    form = LoginForm(form_submited)
    if form.validate():
        user = user_service.get_user_by_email(form_submited['email'])
        if user and user_service.check_login(user, form_submited['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'senha invalida'
    return 'arroz'


@app.route('/inscrever-se', methods=['GET'])
def signup():
    """Signup view"""
    form = UserForm()
    return render_template('signup.html', form=form, title="Cadastrar-se")


@app.route('/cadastrar-action', methods=['POST'])
def signup_action():
    """Action for signup user"""
    try:
        request_form = request.form
        form = UserForm(request_form)
        if form.validate():
            user = user_service.insert_user(request_form)
            address_service.insert_address(user, request_form)

            return redirect('/listar-usuarios')
        return redirect(url_for('signup'))
    except UserExists as e:
        flash('Usuário já existe')
        return redirect(url_for('signup'))

    except Exception as e:
        flash('Erro ao cadastrar um novo usuário')
        return redirect(url_for('signup'))


@app.route('/listar-usuarios', methods=['GET'])
@login_required
@is_admin
def list_users():
    """List all Users"""
    users = user_service.list()
    return render_template('list-users.html', users=users, title="Listar Usuários")


@app.route('/excluir-usuario/<user_id>', methods=['GET'])
@login_required
@is_admin
def delete_user(user_id: int):
    """Delete an User"""
    user, address = user_service.get_user_with_address(user_id)
    address_service.delete(address.id)
    user_service.delete(user.id)
    return redirect(url_for('list_users'))


@app.route('/editar-usuario/<user_id>', methods=['GET'])
@login_required
@is_admin
def edit_user(user_id: int):
    """Edit an User"""
    try:
        user, address = user_service.get_user_with_address(user_id)
        form = UserForm()
        return render_template('signup.html', user=user, address=address, title="Editar Usuário", form=form)
    except UserNotFound as e:
        flash('Usuário não encontrado')
        return redirect(url_for('list_users'))


@app.route('/editar-perfil', methods=['GET'])
@login_required
def edit_profile():
    """Edit profile of current user"""
    user, address = user_service.get_user_with_address(current_user.id)
    form = UserForm
    return render_template('signup.html', user=user, address=address, title="Editar Perfil", form=form)


@app.route('/editar-perfil-action', methods=['POST'])
@login_required
def edit_profile_action():
    """Edit action profile of current user"""
    try:
        request_form = request.form
        form = UserForm(request_form)
        if form.validate():
            address_id = form['address_id']
            user_service.update_user(current_user.id, form)
            address_service.update_address(address_id, form)
            return redirect(url_for('edit_user', user_id=current_user.id))
        flash('Campos invalidos')
        return redirect(url_for('edit_profile'))
    except Exception as e:
        flash('Erro ao atualizar usuário')
        return redirect(url_for('list_users'))

@app.route('/editar-usuario-action/<user_id>', methods=['POST'])
@login_required
@is_admin
def edit_user_action(user_id):
    """Action for edit user"""
    try:
        request_form = request.form
        form = UserForm(request_form)
        if form.validate():
            address_id = form['address_id']
            user_service.update_user(user_id, form)
            address_service.update_address(address_id, form)
            return redirect(url_for('edit_user', user_id=user_id))
    except Exception as e:
        flash('Erro ao atualizar usuário')
        return redirect(url_for('list_users'))


@app.route('/logout')
def logout():
    """Logout current user"""
    logout_user()
    return redirect('index')
