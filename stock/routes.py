from flask import Blueprint, request, jsonify
from stock.service import get_stock_data  # 株価取得の処理を呼び出す

stock_api = Blueprint("stock_api", __name__)  # Blueprintでルートグループを作成


@stock_api.route("/", methods=["GET"])  # /api/stock/ にGETリクエストが来たら呼ばれる
def get_stock():
    # クエリパラメータを取得。なければデフォルト値を使う
    symbol = request.args.get("symbol", "AAPL")
    period = request.args.get("period", "10d")
    interval = request.args.get("interval", "1d")
    fields = request.args.get("fields", "Open,High,Low,Close,Volume")

    field_list = fields.split(",")

    try:
        # データ取得処理を呼び出し、結果をJSONで返す
        result = get_stock_data(symbol, period, interval, field_list)
        return jsonify(result)
    except Exception as e:
        # エラーが起きたら400エラーでメッセージを返す
        return jsonify({"error": str(e)}), 400
