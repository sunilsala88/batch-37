

import yfinance as yf
data=yf.download('BTC-USD',period='10y',multi_level_index=False)
print(data)

import pandas_ta as ta

def sma(closing_price,period):
    return ta.sma(closing_price,length=period)

def ema(closing_price,period):
    return ta.ema(closing_price,length=period)

from backtesting import Backtest, Strategy


class SMAcrossover(Strategy):
    s1=50
    e1=20

    def init(self):
        pass

    def next(self):
        pass


sma=sma(data['Close'],50)
ema=ema(data['Close'],20)
print(sma)
print(ema)

# bt=Backtest(data, SMAcrossover,cash=10_00_000)
# result=bt.run()
# bt.plot()