
from numpy import nan
from pandas import Series
import yfinance as yf


def ema(
	close: Series,
	length: int = 10,
	presma: bool = True,
	offset: int = 0,
	adjust: bool = False,
	fillna=None,
) -> Series:
	"""Standalone Exponential Moving Average without pandas_ta dependency."""
	if close is None:
		return None
	if not isinstance(close, Series):
		close = Series(close)
	if length is None or length <= 0:
		length = 10

	close = close.copy()

	# Mimics TA-Lib style EMA seed using SMA at the first valid EMA point.
	if presma and length > 1 and len(close) >= length:
		sma_nth = close.iloc[:length].mean()
		close.iloc[: length - 1] = nan
		close.iloc[length - 1] = sma_nth

	ema_series = close.ewm(span=length, adjust=adjust).mean()

	if offset != 0:
		ema_series = ema_series.shift(offset)

	if fillna is not None:
		ema_series = ema_series.fillna(fillna)

	ema_series.name = f"EMA_{length}"
	return ema_series


data = yf.download("TSLA", period="3y", interval="1d", multi_level_index=False)
print(data)

data["sma1"] = data["Close"].rolling(10).mean()
data["sma2"] = data["Close"].rolling(10).mean()
data["ema"] = ema(data["Close"], length=10)

import pandas_ta as ta
data["ema_ta"] = ta.ema(data["Close"], length=10)
import talib as ta1

data["ema_talib"] = ta1.EMA(data["Close"], timeperiod=10)
print(data)

#plotly
#matplotlib
#mplfinance
import mplfinance as mpf
a=mpf.make_addplot(data["sma1"],color='blue')
b=mpf.make_addplot(data["ema"],color='red')
mpf.plot(data,type='candle',style='yahoo', addplot=[a,b])


#bollinger band