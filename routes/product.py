from flask import Blueprint, render_template, request, redirect, url_for, flash
from peewee import DoesNotExist
from models import Product

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


# 新規追加：削除機能
@product_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete(product_id):
    """
    指定された製品IDの製品をデータベースから削除する。
    """
    try:
        # 製品を取得
        product = Product.get_by_id(product_id)
        name = product.name
        
        # 製品を削除
        product.delete_instance()
        
        # 成功メッセージを設定
        flash(f'製品「{name}」を削除しました。', 'success')
        
    except DoesNotExist:
        # 製品が見つからなかった場合のエラーメッセージ
        flash('指定された製品が見つかりません。', 'error')
    
    # 製品一覧画面にリダイレクト
    return redirect(url_for('product.list'))


@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', title='製品一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Product.create(name=name, price=price)
        return redirect(url_for('product.list'))
    
    return render_template('product_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)