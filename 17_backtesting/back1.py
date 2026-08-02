

import yfinance as yf
data=yf.download('BTC-USD',period='10y',multi_level_index=False)
print(data)
import time
import pandas_ta as ta

def calculate_sma(closing_price,period):
    return ta.sma(closing_price,length=period)

def calculate_ema(closing_price,period):
    return ta.ema(closing_price,length=period)

from backtesting import Backtest, Strategy


class SMAcrossover(Strategy):
    s1=50
    e1=20

    def init(self):
        closing_price=self.data.Close.s
        self.sma=self.I(calculate_sma,closing_price,self.s1)
        self.ema=self.I(calculate_ema,closing_price,self.e1)

    def next(self):

        current_price=self.data.Close[-1]
        current_sma=self.sma[-1]
        current_ema=self.ema[-1]
        previous_sma=self.sma[-2]
        previous_ema=self.ema[-2]

        if current_ema>current_sma and previous_ema<previous_sma:
            self.buy()

        elif current_ema<current_sma and previous_ema>previous_sma:
            if self.position:
                self.position.close()



sma=calculate_sma(data['Close'],50)
ema=calculate_ema(data['Close'],20)
print(sma)
print(ema)

bt=Backtest(data, SMAcrossover,cash=10_00_000)
result=bt.run()
print(result)
bt.plot()