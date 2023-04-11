from app import app, is_admin, csrf
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app.services.order_service import OrderService

order_service = OrderService()

@login_required
@csrf.exempt
@app.route('/pedidos', methods=['POST'])
def create_order():
    try:
        products = request.json['products']

        if not products:
            return jsonify({
                "message": "Não há produtos.",
                "error": 1
            }), 400

        order = order_service.store_order(products)

        return jsonify({
            "error": 0,
            "order_id": order.id
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Ocorreu um erro inesperado ao tentar criar o pedido",
            "error": 1
        }), 500


@login_required
@app.route('/pedidos')
def list_orders():
    orders = []

    if current_user.is_admin():
        orders = order_service.list()

    return render_template('list-orders.html', orders=orders)