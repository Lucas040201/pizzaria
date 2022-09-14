from app import app, is_admin
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.product_service import ProductService

product_service = ProductService()


@app.route('/listar-produtos', methods=['GET'])
def list_products():
    """List all products"""
    products = product_service.list()
    return render_template('list-products.html', products=products)


@app.route('/cadastrar-produto', methods=['GET'])
@login_required
@is_admin
def store_product():
    """Store product view"""
    return render_template('store-product.html')


@app.route('/cadastrar-produto-action', methods=['POST'])
@login_required
@is_admin
def store_product_action():
    """Action for store product"""
    try:
        form = request.form
        if not 'image' in request.files:
            flash('Por favor, insira uma imagem')
            redirect(url_for('store_product'))

        file = request.files
        inserted_product = product_service.insert_product(form, file)
        return redirect(url_for('list_products'))
    except Exception as e:
        flash('Erro ao cadastrar Produto')
        return redirect(url_for('store_product'))


@app.route('/editar-produto/<product_id>', methods=['GET'])
@login_required
@is_admin
def edit_product(product_id):
    """Edit product view"""
    product = product_service.show(product_id)

    if not product:
        flash('Produto não encontrado')
        return redirect(url_for('store_product'))

    return render_template('store-product.html', product=product)


@app.route('/editar-produto-action/<product_id>', methods=['POST'])
@login_required
@is_admin
def edit_product_action(product_id):
    """Action for edit product"""
    try:
        data = request.form
        file = request.files

        if not file['image']:
            file = None

        updated = product_service.update_product(product_id, data, file)
        return redirect(url_for('edit_product'), product_id=product_id)
    except Exception as e:
        flash('Erro ao atualizar Produto')
        return redirect(url_for('edit_product'), product_id=product_id)


@app.route('/excluir-produto/<product_id>', methods=['GET'])
@login_required
@is_admin
def delete_product(product_id):
    """Delete product"""
    product_service.delete(product_id)
    return redirect(url_for('store_product'))
