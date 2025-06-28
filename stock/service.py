import yfinance as yf


def get_stock_data(symbol: str, period: str, interval: str, fields: list[str]):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)

    if df.empty:
        raise ValueError(
            "取得されたデータが空です。symbol, period, interval を確認してください。"
        )

    # reset_indexでDate列を作成
    df = df.reset_index()

    # "Date"列がdatetime型かチェックし、必要なら変換
    if "Date" in df.columns and not df["Date"].dtype == "O":
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    elif "Datetime" in df.columns:
        df.rename(columns={"Datetime": "Date"}, inplace=True)
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError(
            "データに日付列が含まれていません。intervalの指定を確認してください。"
        )

    # 必要な列だけ抽出（存在するものだけ）
    available_fields = df.columns.intersection(fields + ["Date"])
    result_df = df[available_fields].copy()

    return result_df.to_dict(orient="records")
