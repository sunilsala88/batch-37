


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


def hl2(high, low):
	high = pd.Series(high) if high is not None else None
	low = pd.Series(low) if low is not None else None
	if high is None or low is None:
		return None
	return (high + low) / 2.0


def supertrend(
	high,
	low,
	close,
	length=None,
	atr_length=None,
	multiplier=None,
	atr_mamode=None,
	offset=None,
	**kwargs,
):
	"""Supertrend (pandas-only implementation, pandas_ta compatible signature)."""
	length = int(length) if length and int(length) > 0 else 7
	atr_length = int(atr_length) if atr_length and int(atr_length) > 0 else length
	high = pd.Series(high) if high is not None else None
	low = pd.Series(low) if low is not None else None
	close = pd.Series(close) if close is not None else None

	if high is None or low is None or close is None or len(close) < (length + 1):
		return None

	multiplier = float(multiplier) if multiplier and float(multiplier) > 0 else 3.0
	atr_mamode = (atr_mamode or "rma").lower()
	offset = int(offset) if offset else 0

	m = close.size
	dir_ = [1] * m
	trend = [0] * m
	long = [np.nan] * m
	short = [np.nan] * m

	hl2_ = hl2(high, low)
	matr = multiplier * atr(high, low, close, atr_length, mamode=atr_mamode)
	lb = hl2_ - matr
	ub = hl2_ + matr

	for i in range(1, m):
		if close.iat[i] > ub.iat[i - 1]:
			dir_[i] = 1
		elif close.iat[i] < lb.iat[i - 1]:
			dir_[i] = -1
		else:
			dir_[i] = dir_[i - 1]
			if dir_[i] > 0 and lb.iat[i] < lb.iat[i - 1]:
				lb.iat[i] = lb.iat[i - 1]
			if dir_[i] < 0 and ub.iat[i] > ub.iat[i - 1]:
				ub.iat[i] = ub.iat[i - 1]

		if dir_[i] > 0:
			trend[i] = long[i] = lb.iat[i]
		else:
			trend[i] = short[i] = ub.iat[i]

	trend[0] = np.nan
	dir_[:length] = [np.nan] * length

	_props = f"_{length}_{multiplier}"
	data = {
		f"SUPERT{_props}": trend,
		f"SUPERTd{_props}": dir_,
		f"SUPERTl{_props}": long,
		f"SUPERTs{_props}": short,
	}
	df = pd.DataFrame(data, index=close.index)

	df.name = f"SUPERT{_props}"
	df.category = "overlap"

	if offset != 0:
		df = df.shift(offset)

	if "fillna" in kwargs:
		df.fillna(kwargs["fillna"], inplace=True)

	return df

data=yf.download("TSLA",period="3y",interval="1d",multi_level_index=False)
print(data)

rsi1=atr(data['High'],data['Low'],data['Close'],length=14)
print(rsi1)

super1=supertrend(data['High'],data['Low'],data['Close'],length=14, multiplier=3.0)
print(super1)

import pandas_ta as ta
super1=ta.supertrend(data['High'],data['Low'],data['Close'],length=14, multiplier=3.0)
print(super1)





# l=mpf.make_addplot(super1["SUPERTl_14_3.0"],color='blue')
# s=mpf.make_addplot(super1["SUPERTs_14_3.0"],color='black')

# mpf.plot(data,type='candle',style='yahoo', addplot=[l,s])


adx1=ta.adx(data['High'],data['Low'],data['Close'],length=14)
print(adx1)


l=mpf.make_addplot(adx1["ADX_14"],color='blue',panel=1)


# mpf.plot(data,type='candle',style='yahoo', addplot=[l])

donchain1=ta.donchian(data['High'],data['Low'],data['Close'],lower_length=30)
print(donchain1)