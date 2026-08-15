import yfinance as yf
import pandas as pd
from backtesting import Backtest, Strategy


def get_tsla_1min_candles(period="7d", interval="1m"):
    df = yf.download("TSLA", period=period, interval=interval)

    # Flatten MultiIndex columns (yfinance returns (field, ticker) tuples)
    if df.columns.nlevels > 1:
        df.columns = [col[0] for col in df.columns]

    return df


df = get_tsla_1min_candles()

# backtesting.py requires columns: Open, High, Low, Close, (Volume)
df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()


class OpeningRangeBreakout(Strategy):
    # Length of the opening range in minutes
    or_minutes =60

    # Stop taking new trades / flatten this many minutes before the session's
    # last bar. Orders fill at the *next* bar's open, so flattening a few
    # minutes early (instead of on the very last bar) keeps the exit fill
    # inside the same trading day instead of leaking into next day's open.
    flatten_minutes_before_close = 5

    def init(self):
        # Track the date of each bar so we know when a new trading day starts
        self._dates = pd.Series(self.data.index.date, index=self.data.index)

        # Last timestamp of each trading day, known upfront from the full
        # index (available in init() before the data gets walked bar-by-bar)
        self._day_end_time = pd.Series(self.data.index, index=self.data.index.date)
        self._day_end_time = self._day_end_time.groupby(level=0).max()

        # State reset per trading day
        self._current_day = None
        self._bars_since_open = 0
        self._or_high = None
        self._or_low = None
        self._or_set = False  # whether the opening range has been finalized

    def next(self):
        i = len(self.data) - 1
        bar_time = self.data.index[-1]
        bar_date = self._dates.iloc[i]

        # New trading day -> reset the opening range state
        if bar_date != self._current_day:
            self._current_day = bar_date
            self._bars_since_open = 0
            self._or_high = -float("inf")
            self._or_low = float("inf")
            self._or_set = False

        self._bars_since_open += 1

        # Still inside the opening range window -> just update high/low
        if self._bars_since_open <= self.or_minutes:
            self._or_high = max(self._or_high, self.data.High[-1])
            self._or_low = min(self._or_low, self.data.Low[-1])
            if self._bars_since_open == self.or_minutes:
                self._or_set = True
            return

        # Opening range not established yet (e.g. gap in data) -> skip
        if not self._or_set:
            return

        # Inside the closing window -> flatten and stop trading for the day
        day_end = self._day_end_time[bar_date]
        in_closing_window = bar_time >= day_end - pd.Timedelta(
            minutes=self.flatten_minutes_before_close
        )
        if in_closing_window:
            if self.position:
                self.position.close()
            return

        price = self.data.Close[-1]

        # Breakout above the opening range high -> go long
        if not self.position and price > self._or_high:
            self.buy(sl=self._or_low)

        # Breakout below the opening range low -> go short
        elif not self.position and price < self._or_low:
            self.sell(sl=self._or_high)


bt = Backtest(df, OpeningRangeBreakout, cash=100_000, commission=0.0002, finalize_trades=True)
stats = bt.run()

print(stats)
print(stats._trades)

bt.plot()
