from flask import Flask
from flask_cors import CORS
from stock.routes import stock_api  # ルート定義をインポート

app = Flask(__name__)  # Flaskアプリ本体を作る
CORS(app)  # Reactなど別ドメインからのアクセスを許可

# /api/stock へのアクセスを stock_api Blueprint に任せる
app.register_blueprint(stock_api, url_prefix="/api/stock")


@app.route("/health")  # サーバーの動作確認用エンドポイント
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)  # 開発用サーバーを起動
