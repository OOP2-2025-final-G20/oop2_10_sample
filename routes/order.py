from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        order_date = datetime.now()
        
        # --- 修正箇所: quantity=1 を追加しました ---
        # これでデータベースの「個数必須」ルールを守れます
        Order.create(
            user=user_id, 
            product=product_id, 
            order_date=order_date, 
            quantity=1
        )
        
        return redirect(url_for('order.list'))
    
    users = User.select()
    products = Product.select()
    return render_template('order_add.html', users=users, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        order.user = request.form['user_id']
        order.product = request.form['product_id']
        # 編集時も必要であればここで order.quantity = ... を更新できますが、
        # 今回のエラー回避には影響しないためそのままでOKです
        order.save()
        return redirect(url_for('order.list'))

    users = User.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, users=users, products=products)