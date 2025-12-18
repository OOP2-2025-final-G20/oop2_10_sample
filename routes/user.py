from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    
    # データ取得
    users = User.select()

    return render_template('user_list.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        User.create(name=name, age=age, email=email if email else None, address=address if address else None)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.email = request.form.get('email', '') or None
        user.address = request.form.get('address', '') or None
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    user = User.get_or_none(User.id == user_id)
    if user:
        user.delete_instance()
    return redirect(url_for('user.list'))