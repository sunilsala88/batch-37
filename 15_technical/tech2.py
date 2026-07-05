
import yfinance as yf
import mplfinance as mpf
import pandas_ta as ta

data = yf.download("META", period="3y", interval="1d", multi_level_index=False)
print(data)

bb=ta.bbands(data['Close'],length=10)
print(bb)


# a=mpf.make_addplot(bb["BBL_10_2.0_2.0"],color='blue')
# b=mpf.make_addplot(bb["BBM_10_2.0_2.0"],color='black')
# c=mpf.make_addplot(bb["BBU_10_2.0_2.0"],color='yellow')
# mpf.plot(data,type='candle',style='yahoo', addplot=[a,b,c])



#rsi