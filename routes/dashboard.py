from flask import Blueprint
from models import Order, User, Product
from peewee import JOIN

# ダッシュボード専用 Blueprint
# ※ ルーティングは持たず、データ取得専用
dashboard_bp = Blueprint('dashboard', __name__)

def get_recent_orders(limit=20):
    """
    直近の注文を新しい順で取得する
    取得項目：
      - 顧客名
      - 製品名
      - 注文日時

    :param limit: 取得件数（デフォルト20件）
    :return: Peewee Query
    """
    return (
        Order
        .select(Order, User, Product)
        .join(User, JOIN.LEFT_OUTER)
        .switch(Order)
        .join(Product, JOIN.LEFT_OUTER)
        .order_by(Order.order_date.desc())
        .limit(limit)
    )
