import yfinance as yf
import pandas_ta as ta
import vectorbt as vbt

# Same data / same strategy as back2.py (RSIStrategy, backtesting.py version)
data = yf.download('GOOG', period='1y', interval='1h', multi_level_index=False)
print(data)

close = data['Close']

rsi_period = 14
upper = 80
lower = 20

rsi = ta.rsi(close, length=rsi_period)
print(rsi)

# back2.py logic, translated to vectorbt entry/exit signals:
#   RSI > upper  -> close any open position, go long   (long entry / short exit)
#   RSI < lower  -> close any open position, go short  (short entry / long exit)
long_entries = rsi > upper
short_entries = rsi < lower

bt = vbt.Portfolio.from_signals(
    close=close,
    entries=long_entries,
    exits=short_entries,
    short_entries=short_entries,
    short_exits=long_entries,
    init_cash=10_00_000,
    fees=0.002,          # matches commission=0.002 in back2.py
    freq='1h',
)

print(bt.stats())

trades = bt.trades.records_readable
print(trades)
trades.to_csv('trades1.csv', index=False)
print("Saved trades to trades1.csv")
# bt.plot().show()
