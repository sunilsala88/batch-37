
import yfinance as yf
import mplfinance as mpf
import pandas_ta as ta
import pandas as pd


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


def _build_signals(
	indicator,
	xa=80,
	xb=20,
	xseries=None,
	xseries_a=None,
	xseries_b=None,
	cross_values=False,
	cross_series=True,
	offset=0,
):
	out = pd.DataFrame(index=indicator.index)

	if xseries_a is not None:
		xa_cmp = pd.Series(xseries_a, index=indicator.index)
	elif xseries is not None:
		xa_cmp = pd.Series(xseries, index=indicator.index)
	else:
		xa_cmp = pd.Series(float(xa), index=indicator.index)

	if xseries_b is not None:
		xb_cmp = pd.Series(xseries_b, index=indicator.index)
	elif xseries is not None:
		xb_cmp = pd.Series(xseries, index=indicator.index)
	else:
		xb_cmp = pd.Series(float(xb), index=indicator.index)

	out["RSI_A"] = indicator > xa_cmp
	out["RSI_B"] = indicator < xb_cmp

	if cross_values:
		out["RSI_XA"] = (indicator > xa_cmp) & (indicator.shift(1) <= xa_cmp.shift(1))
		out["RSI_XB"] = (indicator < xb_cmp) & (indicator.shift(1) >= xb_cmp.shift(1))

	if cross_series and xseries is not None:
		xs = pd.Series(xseries, index=indicator.index)
		out["RSI_XS_UP"] = (indicator > xs) & (indicator.shift(1) <= xs.shift(1))
		out["RSI_XS_DN"] = (indicator < xs) & (indicator.shift(1) >= xs.shift(1))

	if offset:
		out = out.shift(offset)

	return out


def rsi(
	close,
	length=None,
	scalar=None,
	mamode=None,
	talib=None,
	drift=None,
	offset=None,
	**kwargs,
):
	"""Relative Strength Index (pandas-only implementation, pandas_ta compatible signature)."""
	length = int(length) if length and int(length) > 0 else 14
	close = pd.Series(close) if close is not None else None
	if close is None or close.size < (length + 1):
		return None

	scalar = float(scalar) if scalar is not None else 100.0
	mamode = (mamode or "rma").lower()
	drift = int(drift) if drift and int(drift) > 0 else 1
	offset = int(offset) if offset else 0

	delta = close.diff(drift)
	positive = delta.copy()
	negative = delta.copy()
	positive[positive < 0] = 0
	negative[negative > 0] = 0

	positive_avg = _ma(mamode, positive, length)
	negative_avg = _ma(mamode, negative, length)
	rsi_out = scalar * positive_avg / (positive_avg + negative_avg.abs())

	if offset != 0:
		rsi_out = rsi_out.shift(offset)

	if "fillna" in kwargs:
		rsi_out = rsi_out.fillna(kwargs["fillna"])

	rsi_out.name = f"RSI_{length}"
	rsi_out.category = "momentum"

	signal_indicators = kwargs.pop("signal_indicators", False)
	if not signal_indicators:
		return rsi_out

	signalsdf = pd.concat(
		[
			pd.DataFrame({rsi_out.name: rsi_out}),
			_build_signals(
				indicator=rsi_out,
				xa=kwargs.pop("xa", 80),
				xb=kwargs.pop("xb", 20),
				xseries=kwargs.pop("xseries", None),
				xseries_a=kwargs.pop("xseries_a", None),
				xseries_b=kwargs.pop("xseries_b", None),
				cross_values=kwargs.pop("cross_values", False),
				cross_series=kwargs.pop("cross_series", True),
				offset=offset,
			),
		],
		axis=1,
	)
	return signalsdf

data = yf.download("META", period="3y", interval="1d", multi_level_index=False)
print(data)

bb=ta.bbands(data['Close'],length=10)
print(bb)


# a=mpf.make_addplot(bb["BBL_10_2.0_2.0"],color='blue')
# b=mpf.make_addplot(bb["BBM_10_2.0_2.0"],color='black')
# c=mpf.make_addplot(bb["BBU_10_2.0_2.0"],color='yellow')
# mpf.plot(data,type='candle',style='yahoo', addplot=[a,b,c])



#rsi

rsi1=rsi(data['Close'],length=14)
print(rsi1)

# import pandas_ta as ta
# rsi2=ta.rsi(data['Close'],length=14)
# print(rsi2)


# c=mpf.make_addplot(rsi1,color='black',panel=1)
# mpf.plot(data,type='candle',style='yahoo', addplot=[c])
