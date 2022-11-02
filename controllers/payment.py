from app import app, is_admin, csrf
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app.services.order_service import OrderService

order_service = OrderService()



@app.route('/pagamento/confirmar', methods=['GET'])
def payment_confirm():
    return render_template('payment-confirm.html')


