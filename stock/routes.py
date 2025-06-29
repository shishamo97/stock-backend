from flask import Blueprint, request, jsonify
from stock.service import get_stock_info, get_stock_history, get_stock_symbols

stock_api = Blueprint("stock_api", __name__)  # Blueprintでルートグループを作成


# 企業情報を取得
@stock_api.route("/<symbol>/info", methods=["GET"])
def get_stock_info_route(symbol):
    try:
        result = get_stock_info(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 株価履歴を取得
@stock_api.route("/<symbol>/history", methods=["GET"])
def get_stock_history_route(symbol):
    # クエリパラメータを取得。なければデフォルト値を使う
    period = request.args.get("period", "10d")
    interval = request.args.get("interval", "1d")
    fields = request.args.get("fields", "Open,High,Low,Close,Volume")
    field_list = fields.split(",")

    try:
        # データ取得処理を呼び出し、結果をJSONで返す
        result = get_stock_history(symbol, period, interval, field_list)
        return jsonify(result)
    except Exception as e:
        # エラーが起きたら400エラーでメッセージを返す
        return jsonify({"error": str(e)}), 400


# シンボルを取得
@stock_api.route("/symbols", methods=["GET"])
def get_stock_symbols_route():
    try:
        result = get_stock_symbols()
        return jsonify(result)
    except Exception as e:
        # エラーが起きたら400エラーでメッセージを返す
        return jsonify({"error": str(e)}), 400
