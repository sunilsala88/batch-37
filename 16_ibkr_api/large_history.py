from datetime import datetime, timedelta

from ib_async import IB, Stock, util

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=3)

contract = Stock('TSLA', 'SMART', 'USD')
ib.qualifyContracts(contract)

target_start = datetime.now() - timedelta(days=365)

all_bars = []
end_date_time = ''  # '' means now; walks backwards each iteration

while True:
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=end_date_time,
        durationStr='1 W',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1,
        timeout=60
    )

    if not bars:
        print('no more data returned, stopping')
        break

    all_bars = list(bars) + all_bars

    earliest = bars[0].date
    print(f'fetched {len(bars)} bars, earliest: {earliest}')

    if earliest.replace(tzinfo=None) <= target_start:
        break

    end_date_time = earliest
    ib.sleep(2)  # pacing: stay under 60 requests per 10 min

ib.disconnect()

df = util.df(all_bars)
df = df.drop_duplicates(subset='date').sort_values('date').reset_index(drop=True)

print(df.shape)
print(df.head())
print(df.tail())

df.to_csv('tsla_1min_1year.csv', index=False)
