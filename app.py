from flask import Flask, render_template

from models import initialize_database
from routes import blueprints

# ダッシュボード用（routes/dashboard.py）
from routes.dashboard import get_recent_orders

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各 Blueprint をアプリケーションに登録
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
