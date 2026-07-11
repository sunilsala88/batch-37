


#atr->
#supertrend

import yfinance as yf
import mplfinance as mpf

import pandas as pd
import numpy as np


def _ma(mode, series, length):
	mode = (mode or "rma").lower()
	if mode == "rma":
		alpha = 1.0 / float(length)
		return series.ewm(alpha=alpha, adjust=False, min_periods=length).mean()
	if mode == "ema":
		return series.ewm(span=length, adjust=False, min_periods=length).mean()
	if mode == "sma":
		return series.rolling(length, min_periods=length).mean()
	if mode == "wma":
		weights = pd.Series(range(1, length + 1), dtype="float64")
		return series.rolling(length, min_periods=length).apply(
			lambda x: (x * weights).sum() / weights.sum(), raw=False
		)
	raise ValueError("mamode must be one of: rma, ema, sma, wma")


def true_range(high, low, close, talib=None, prenan=False, drift=None):
	high = pd.Series(high) if high is not None else None
	low = pd.Series(low) if low is not None else None
	close = pd.Series(close) if close is not None else None
	if high is None or low is None or close is None:
		return None

	drift = int(drift) if drift and int(drift) > 0 else 1
	prev_close = close.shift(drift)
	tr = pd.concat(
		[
			(high - low).abs(),
			(high - prev_close).abs(),
			(low - prev_close).abs(),
		],
		axis=1,
	).max(axis=1)

	if prenan:
		tr.iloc[:drift] = np.nan

	tr.name = f"TRUERANGE_{drift}"
	tr.category = "volatility"
	return tr


def atr(
	high,
	low,
	close,
	length=None,
	mamode=None,
	talib=None,
	prenan=None,
	drift=None,
	offset=None,
	**kwargs,
):
	"""Average True Range (pandas-only implementation, pandas_ta compatible signature)."""
	length = int(length) if length and int(length) > 0 else 14
	high = pd.Series(high) if high is not None else None
	low = pd.Series(low) if low is not None else None
	close = pd.Series(close) if close is not None else None

	if high is None or low is None or close is None or len(close) < (length + 1):
		return None

	mamode = (mamode or "rma").lower()
	prenan = bool(prenan) if prenan is not None else False
	drift = int(drift) if drift and int(drift) > 0 else 1
	offset = int(offset) if offset else 0

	tr = true_range(high=high, low=low, close=close, talib=talib, prenan=prenan, drift=drift)
	if tr is None or tr.isna().all():
		return None

	presma = kwargs.pop("presma", True)
	if presma:
		sma_nth = tr.iloc[0:length].mean()
		tr = tr.copy()
		tr.iloc[: length - 1] = np.nan
		tr.iloc[length - 1] = sma_nth

	atr_out = _ma(mamode, tr, length=length)
	if atr_out.isna().all():
		return None

	percent = kwargs.pop("percent", False)
	if percent:
		atr_out = atr_out * (100.0 / close)

	if offset != 0:
		atr_out = atr_out.shift(offset)

	if "fillna" in kwargs:
		atr_out = atr_out.fillna(kwargs["fillna"])

	atr_out.name = f"ATR{mamode[0]}{'p' if percent else ''}_{length}"
	atr_out.category = "volatility"
	return atr_out

data=yf.download("TSLA",period="3y",interval="1d",multi_level_index=False)
print(data)

rsi1=atr(data['High'],data['Low'],data['Close'],length=14)
print(rsi1)


import pandas_ta as ta
rsi2=ta.atr(data['High'],data['Low'],data['Close'],length=14)
print(rsi2)

super1=ta.supertrend(data['High'],data['Low'],data['Close'],length=14, multiplier=3.0)
print(super1)


l=mpf.make_addplot(super1["SUPERTl_14_3.0"],color='blue')
s=mpf.make_addplot(super1["SUPERTs_14_3.0"],color='black')

mpf.plot(data,type='candle',style='yahoo', addplot=[l,s])