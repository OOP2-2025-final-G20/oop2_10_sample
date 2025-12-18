from flask import Flask, render_template

from models import initialize_database
from flask import Flask, render_template, jsonify
from models import initialize_database, Order, Product, User, db
from routes import blueprints
from peewee import fn
from datetime import datetime
from collections import defaultdict
from decimal import Decimal

# --- Peewee用のインポート ---
from peewee import fn  # 集計関数（SUMなど）を使うため
from models.user import User
from models.order import Order
from models.product import Product
# ---------------------------

# ダッシュボード用（routes/dashboard.py）
from routes.dashboard import get_recent_orders

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各 Blueprint をアプリケーションに登録
# リクエスト前にデータベース接続を確認
@app.before_request
def before_request():
    if db.is_closed():
        db.connect()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページ（ダッシュボード）
@app.route('/')
def index():
    # 直近20件の注文を新しい順で取得
    recent_orders = get_recent_orders(limit=20)

    return render_template(
        'index.html',
        recent_orders=recent_orders
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    # --- Peeweeを使ったランキング集計ロジック ---
    
    # User(顧客) を起点に、Order(注文) -> Product(製品) を結合(JOIN)する
    # Product.price を合計して、売上の多い順に5件取得
    
    query = (User
             .select(User.name, fn.SUM(Product.price).alias('total_sales'))
             .join(Order)
             .join(Product)
             .group_by(User)
             .order_by(fn.SUM(Product.price).desc())
             .limit(5))

    ranking_data = []
    for user in query:
        # Peeweeでは .alias('total_sales') で付けた名前に直接アクセスできます
        ranking_data.append({
            'name': user.name,
            'total': int(user.total_sales or 0)
        })

    # 製品のランキングデータ（売上数量で集計）
    product_ranking = []
    try:
        product_sales = (Order
            .select(Product.name, fn.SUM(Order.quantity).alias('total_quantity'))
            .join(Product)
            .group_by(Product.id, Product.name)
            .order_by(fn.SUM(Order.quantity).desc()))
        
        for sale in product_sales:
            product_ranking.append({
                'name': sale.product.name,
                'quantity': sale.total_quantity
            })
    except Exception as e:
        product_ranking = []
    
    # 月別売上データ（月ごとの売上と製品別内訳）
    monthly_sales = []
    try:
        # 月別の売上を取得
        orders_by_month = (Order
            .select(
                fn.strftime('%Y-%m', Order.order_date).alias('month'),
                Product.name,
                fn.SUM(Order.quantity).alias('quantity')
            )
            .join(Product)
            .group_by(fn.strftime('%Y-%m', Order.order_date), Product.id, Product.name)
            .order_by(fn.strftime('%Y-%m', Order.order_date)))
        
        # 月ごとにデータを整理
        monthly_dict = defaultdict(lambda: defaultdict(int))
        for order in orders_by_month:
            monthly_dict[order.month][order.product.name] = order.quantity
        
        # リスト形式に変換
        for month, products in sorted(monthly_dict.items()):
            monthly_sales.append({
                'month': month,
                'products': dict(products)
            })
    except Exception as e:
        monthly_sales = []
    
    # 日別売上データ（日ごとの売上と製品別内訳）
    daily_sales = []
    try:
        # 日別の売上を取得
        orders_by_day = (Order
            .select(
                fn.strftime('%Y-%m-%d', Order.order_date).alias('day'),
                Product.name,
                fn.SUM(Order.quantity).alias('quantity')
            )
            .join(Product)
            .group_by(fn.strftime('%Y-%m-%d', Order.order_date), Product.id, Product.name)
            .order_by(fn.strftime('%Y-%m-%d', Order.order_date)))
        
        # 日ごとにデータを整理
        daily_dict = defaultdict(lambda: defaultdict(int))
        for order in orders_by_day:
            daily_dict[order.day][order.product.name] = order.quantity
        
        # リスト形式に変換（最新30日分に制限）
        sorted_days = sorted(daily_dict.items())
        for day, products in sorted_days[-30:]:  # 最新30日分のみ表示
            daily_sales.append({
                'day': day,
                'products': dict(products)
            })
    except Exception as e:
        daily_sales = []
    
    # 統計情報の取得
    stats = {}
    try:
        # 総売上金額（注文数量 × 製品価格の合計）
        total_revenue = (Order
            .select(fn.SUM(Order.quantity * Product.price).alias('total'))
            .join(Product)
            .scalar())
        stats['total_revenue'] = float(total_revenue) if total_revenue else 0.0
        
        # 総注文数
        stats['total_orders'] = Order.select().count()
        
        # 総ユーザー数
        stats['total_users'] = User.select().count()
        
        # 総製品数
        stats['total_products'] = Product.select().count()
    except Exception as e:
        stats = {
            'total_revenue': 0.0,
            'total_orders': 0,
            'total_users': 0,
            'total_products': 0
        }
    
    return render_template('index.html', 
                         ranking_data=ranking_data,
                         product_ranking=product_ranking,
                         monthly_sales=monthly_sales,
                         daily_sales=daily_sales,
                         stats=stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
