
import yfinance as yf
import mplfinance as mpf

import pandas as pd
import numpy as np




data=yf.download("TSLA",period="3y",interval="1d",multi_level_index=False)
print(data)


def donchian(
	high,
	low,
	close=None,
	lower_length=None,
	upper_length=None,
	offset=None,
	**kwargs,
):
	"""Donchian Channel (pandas-only implementation, pandas_ta compatible signature)."""
	high = pd.Series(high) if high is not None else None
	low = pd.Series(low) if low is not None else None

	if high is None or low is None:
		return None

	lower_length = int(lower_length) if lower_length and int(lower_length) > 0 else 20
	upper_length = int(upper_length) if upper_length and int(upper_length) > 0 else lower_length
	offset = int(offset) if offset else 0

	lower = low.rolling(window=lower_length, min_periods=lower_length).min()
	upper = high.rolling(window=upper_length, min_periods=upper_length).max()
	middle = (lower + upper) / 2.0

	_props = f"_{lower_length}_{upper_length}"
	df = pd.DataFrame(
		{
			f"DCL{_props}": lower,
			f"DCM{_props}": middle,
			f"DCU{_props}": upper,
		},
		index=high.index,
	)

	df.name = f"DC{_props}"
	df.category = "volatility"

	if offset != 0:
		df = df.shift(offset)

	if "fillna" in kwargs:
		df.fillna(kwargs["fillna"], inplace=True)

	return df


donchain1=donchian(data['High'],data['Low'],data['Close'],lower_length=30)
print(donchain1)


l=mpf.make_addplot(donchain1["DCL_30_30"],color='blue')
s=mpf.make_addplot(donchain1["DCU_30_30"],color='black')

mpf.plot(data,type='candle',style='yahoo', addplot=[l,s])
