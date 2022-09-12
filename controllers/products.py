from app import app
from flask import render_template, request, flash, redirect, url_for
from app.services.product_service import ProductService

product_service = ProductService()


@app.route('/listar-produtos', methods=['GET'])
def list_products():
    products = product_service.list()
    return render_template('list-products.html', products=products)


@app.route('/cadastrar-produto', methods=['GET'])
def store_product():
    return render_template('store-product.html')


@app.route('/cadastrar-produto-action', methods=['POST'])
def store_product_action():
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
def edit_product(product_id):
    product = product_service.show(product_id)

    if not product:
        flash('Produto não encontrado')
        return redirect(url_for('store_product'))

    return render_template('store-product.html', product=product)

@app.route('/editar-produto-action/<product_id>', methods=['POST'])
def edit_product_action(product_id):
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
def delete_product(product_id):
    product_service.delete(product_id)
    return redirect(url_for('store_product'))
