import backtrader as bt
import yfinance as yf


class RSIStrategy(bt.Strategy):
    params = dict(
        rsi_period=14,
        upper=80,
        lower=20,
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.rsi_period)

    def next(self):
        current_rsi = self.rsi[0]

        if current_rsi > self.p.upper:
            if self.position:
                self.close()
            self.buy()

        elif current_rsi < self.p.lower:
            if self.position:
                self.close()
            self.sell()


data = yf.download('GOOG', period='1y', interval='1h', multi_level_index=False)
print(data)

feed = bt.feeds.PandasData(dataname=data)

cerebro = bt.Cerebro()
cerebro.adddata(feed)
cerebro.addstrategy(RSIStrategy)
cerebro.broker.setcash(10_00_000)
cerebro.broker.setcommission(commission=0.002)

cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
results = cerebro.run()
strat = results[0]
print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

print("Returns:", strat.analyzers.returns.get_analysis())
print("Sharpe:", strat.analyzers.sharpe.get_analysis())
print("Drawdown:", strat.analyzers.drawdown.get_analysis())
print("Trades:", strat.analyzers.trades.get_analysis())

cerebro.plot()
