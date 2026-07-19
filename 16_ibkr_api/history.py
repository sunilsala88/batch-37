from ib_async import IB, Stock, util

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

contract = Stock('TSLA', 'SMART', 'USD')

bars = ib.reqHistoricalData(
    contract,
    endDateTime='20260116 16:00:00',#yyyyMMdd HH:mm:ss
    durationStr='1 M',
    barSizeSetting='5 mins',
    whatToShow='TRADES',
    useRTH=True,
    formatDate=1
)

df = util.df(bars)
print(df)

df.to_csv('tsla_10min_1month.csv', index=False)

ib.disconnect()
