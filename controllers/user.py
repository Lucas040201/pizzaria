from flask import render_template, request, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user
from app import app, is_admin, get_google_provider_cfg, client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

from app.infra.exceptions.user_exists import UserExists
from app.infra.exceptions.user_not_found import UserNotFound

from app.services.address_service import AddressService
from app.services.user_service import UserService

from app.infra.forms.login_form import LoginForm
from app.infra.forms.user_form_register import UserFormRegister
from app.infra.forms.user_form_update import UserFormUpdate

user_service = UserService()
address_service = AddressService()


@app.route('/login', methods=['GET'])
def login():
    """Login view"""
    form = LoginForm()
    return render_template('login.html', form=form, title="Fazer Login")


@app.route('/login-google')
def login_google():
    request_uri = user_service.google_redirect()
    return redirect(request_uri)


@app.route('/login-google/callback')
def login_google_callback():
    try:
        user_service.make_google_login()
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('login'))


@app.route('/login-action', methods=['POST'])
def login_action():
    """Action for user login"""
    try:
        form_submited = request.form

        user_service.make_login(form_submited)

        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('login'))


@app.route('/inscrever-se', methods=['GET'])
def signup():
    """Signup view"""
    form = UserFormRegister()
    return render_template('signup.html', form=form, title="Cadastrar-se")


@app.route('/cadastrar-action', methods=['POST'])
def signup_action():
    """Action for signup user"""
    try:
        request_form = request.form
        form = UserFormRegister(request_form)
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
        form = UserFormUpdate()
        return render_template('signup.html', user=user, address=address, title="Editar Usuário", form=form)
    except UserNotFound as e:
        flash('Usuário não encontrado')
        return redirect(url_for('list_users'))


@app.route('/editar-perfil', methods=['GET'])
@login_required
def edit_profile():
    """Edit profile of current user"""
    form = UserFormUpdate()
    return render_template('signup.html', title="Editar Perfil", form=form)


@app.route('/editar-perfil-action', methods=['POST'])
@login_required
def edit_profile_action():
    """Edit action profile of current user"""
    try:
        request_form = request.form
        form = UserFormUpdate(request_form)
        if form.validate():
            user_service.update_user(current_user.id, request_form)
            if current_user.address:
                address_id = request_form['address_id']
                address_service.update_address(address_id, request_form)
            else:
                address_service.insert_address(current_user, request_form)
            return redirect(url_for('edit_profile'))
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
        form = UserFormUpdate(request_form)

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
