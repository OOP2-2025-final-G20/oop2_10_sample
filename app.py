from flask import Flask, render_template
from models import initialize_database
from routes import blueprints

# --- Peewee用のインポート ---
from peewee import fn  # 集計関数（SUMなど）を使うため
from models.user import User
from models.order import Order
from models.product import Product
# ---------------------------

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
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

    return render_template('index.html', ranking_data=ranking_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)