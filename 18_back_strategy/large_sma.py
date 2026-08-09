import pandas as pd
from backtesting.lib import resample_apply
data = pd.read_csv('/Users/algo trading 2026/batch 37/tsla_1min_1year.csv')
data['date'] = pd.to_datetime(data['date'], utc=True)
data.set_index('date', inplace=True)
data.rename(columns={
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'close': 'Close',
    'volume': 'Volume',
}, inplace=True)
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
    gran='5min'

    def init(self):
        
        self.sma=resample_apply(self.gran, calculate_sma, self.data.Close.s, self.s1)
        self.ema=resample_apply(self.gran, calculate_ema, self.data.Close.s, self.e1)

    def next(self):

        current_price=self.data.Close[-1]
        current_sma=self.sma[-1]
        current_ema=self.ema[-1]
        previous_sma=self.sma[-2]
        previous_ema=self.ema[-2]

        if current_ema>current_sma and previous_ema<previous_sma:
            if self.position:
                self.position.close()
            self.buy()

        elif current_ema<current_sma and previous_ema>previous_sma:
            if self.position:
                self.position.close()

            self.sell()



sma=calculate_sma(data['Close'],50)
ema=calculate_ema(data['Close'],20)
print(sma)
print(ema)

bt=Backtest(data, SMAcrossover,cash=10_00_000,finalize_trades=True)
result=bt.run()
print(result)
# bt.plot()


s1_sample=range(45,70,5)
e1_sample=range(10,40,5)
l1=['5min','15min','30min','60min']
stats=bt.optimize(gran=l1, s1=s1_sample, e1=e1_sample, maximize='Return [%]')
print(stats)
print(stats['_strategy'])
bt.plot()
