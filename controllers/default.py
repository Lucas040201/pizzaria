from app import app
from flask import render_template, request, flash, redirect

from app.exceptions.user_exists import UserExists
from app.infra.entities.role import Role
from app.services.address_service import AddressService
from app.services.product_service import ProductService
from app.services.user_service import UserService

user_service = UserService()
address_service = AddressService()
product_service = ProductService()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inscrever-se', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    try:
        form = request.form
        user = user_service.insert_user(form)
        address = address_service.insert_address(user, form)

        return redirect('/listar-usuarios')
    except UserExists as e:
        flash('Usuário já existe')
        return redirect('/inscrever-se')

    except Exception as e:
        flash('Erro ao cadastrar um novo usuário')
        return redirect('/inscrever-se')


@app.route('/listar-usuarios', methods=['GET'])
def list_users():
    users = user_service.list()
    return render_template('list-users.html', users=users)


@app.route('/excluir-usuarios/<user_id>', methods=['GET'])
def delete_user(user_id):
    user, address = user_service.select_user_with_address(user_id)
    address_service.delete(address.id)
    user_service.delete(user.id)
    return redirect('/listar-usuarios')


@app.route('/editar-usuarios/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        user, address = user_service.select_user_with_address(user_id)
        return render_template('signup.html', user=user, address=address)

    try:
        form = request.form
        address_id = form['address_id']
        user = user_service.update_user(user_id, form)
        address = address_service.update_address(address_id, form)
        return redirect(f"/editar-usuarios/{user_id}")
    except Exception as e:
        flash('Erro ao atualizar usuário')
        return redirect('/listar-usuarios')


@app.route('/listar-produtos', methods=['GET'])
def list_products():
    return render_template('list-products.html')


@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def store_product():
    if request.method == 'GET':
        return render_template('store-product.html')

    try:
        form = request.form
        if not 'image' in request.files:
            flash('Por favor, insira uma imagem')
            redirect('/cadastrar-produto')

        file = request.files

        inserted_product = product_service.insert_product(form, file)
        return 'teste'
    except Exception as e:
        print(e)
        return 'exception'


@app.route('/editar-produto/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'GET':
        return render_template('store-product.html')

    try:
        return redirect(f"/editar-produto/{product_id}")
    except Exception as a:
        pass


@app.route('/excluir-produto/<product_id>', methods=['GET'])
def delete_product(product_id):
    product_service.delete(product_id)
    return redirect('/listar-produtos')
