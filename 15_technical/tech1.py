
#talib
#pandas ta
#ta

import pandas_ta as ta
import yfinance as yf
data=yf.download('TSLA',period='3y',interval='1d',multi_level_index=False)
print(data)

sma1=ta.sma(data['Close'],length=10)
print(sma1.head(20))