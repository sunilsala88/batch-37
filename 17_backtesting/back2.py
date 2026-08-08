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

        if current_rsi > self.upper:
            if self.position:
                self.position.close()
            self.buy()

        elif current_rsi < self.lower:
            if self.position:
                self.position.close()
            self.sell()


rsi = calculate_rsi(data['Close'], 14)
print(rsi)

bt = Backtest(data, RSIStrategy, cash=10_00_000,commission=0.002)
result = bt.run()
print(result)
# bt.plot()
