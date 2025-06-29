import pandas as pd
import yfinance as yf


def get_stock_info(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    if not info:
        raise ValueError("企業情報が取得できませんでした。symbolを確認してください。")

    keys = [
        "longName",
        "marketCap",
        "dividendYield",
        "sector",
        "previousClose",
    ]
    result = {k: info.get(k, None) for k in keys}

    # symbolを付加
    result["symbol"] = symbol

    return result


def get_stock_history(symbol: str, period: str, interval: str, fields: list[str]):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)

    if df.empty:
        raise ValueError(
            "取得されたデータが空です。symbol, period, interval を確認してください。"
        )

    # reset_indexでDate列を作成
    df = df.reset_index()

    # 日付列を"Date"に統一（"Date"または"Datetime"のどちらか）
    if "Date" in df.columns:
        date_col = "Date"
    elif "Datetime" in df.columns:
        df.rename(columns={"Datetime": "Date"}, inplace=True)
        date_col = "Date"
    else:
        raise ValueError(
            "データに日付列が含まれていません。intervalの指定を確認してください。"
        )

    # Date列がdatetime型なら文字列に変換
    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = df[date_col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 抽出対象カラムにDate列を必ず含める
    required_fields = set(fields)
    required_fields.add(date_col)

    # 実際に存在する列だけを抽出
    available_fields = df.columns.intersection(required_fields)
    result_df = df.loc[:, available_fields].copy()

    return result_df.to_dict(orient="records")


def get_stock_symbols():
    return [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
    ]
