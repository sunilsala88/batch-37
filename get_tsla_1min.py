"""
Fetch 1-minute TSLA candle data for the last 7 days using yfinance.

Note: yfinance/Yahoo Finance only allows 1-minute interval data for a
maximum lookback of 7 days, so period='7d' is the max here.
"""

import yfinance as yf

def get_tsla_1min_candles(period="7d", interval="1m"):
    df = yf.download("TSLA", period=period, interval=interval)

    # Flatten MultiIndex columns (yfinance returns (field, ticker) tuples)
    if df.columns.nlevels > 1:
        df.columns = [col[0] for col in df.columns]

    return df


if __name__ == "__main__":
    df = get_tsla_1min_candles()

    print(df.shape)
    print(df.head())
    print(df.tail())

    df.to_csv("tsla_1min_7d.csv")
    print("Saved to tsla_1min_7d.csv")
