import yfinance as yf
data=yf.download('TSLA',period='39d',interval='15m',multi_level_index=False)
data