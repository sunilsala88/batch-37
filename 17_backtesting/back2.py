import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest, Strategy

data = yf.download('GOOG', period='1y', interval='1h', multi_level_index=False)
print(data)


def calculate_rsi(closing_price, period):
    return ta.rsi(closing_price, length=period)


class RSIStrategy(Strategy):
    rsi_period = 14
    upper = 80
    lower = 20

    def init(self):
        closing_price = self.data.Close.s
        self.rsi = self.I(calculate_rsi, closing_price, self.rsi_period)

    def next(self):
        current_rsi = self.rsi[-1]

        # Only flip position on an actual direction change (matches
        # vectorbt's accumulate=False behavior): repeat same-side signals
        # while already positioned that way are ignored, not re-entered.
        if current_rsi > self.upper and not self.position.is_long:
            if self.position:
                self.position.close()
            self.buy()

        elif current_rsi < self.lower and not self.position.is_short:
            if self.position:
                self.position.close()
            self.sell()


rsi = calculate_rsi(data['Close'], 14)
print(rsi)

bt = Backtest(data, RSIStrategy, cash=10_00_000)
result = bt.run()
print(result)

trades = result['_trades']
trades.to_csv('trades2.csv', index=False)

# bt.plot()
