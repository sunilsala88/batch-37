import pendulum as pdlm
import time

from  ib_async import *
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=18)

import indicators as ta



time_frame1=1
tickers = ['ETH','AAVE','BCH','LTC']


time_zone2= 'America/New_York'
# time_zone2= 'Asia/Kolkata'

print(pdlm.now(tz=time_zone2))



def get_historical_data(ticker_contract,bar_size,duration):
    bars = ib.reqHistoricalData(
    ticker_contract, endDateTime='', durationStr=duration,
    barSizeSetting=bar_size, whatToShow='MIDPOINT', useRTH=True,formatDate=1)
    # convert to pandas dataframe:
    df = util.df(bars)
    sup=ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    df['supertrend']=sup['SUPERTd_10_3.0']
    df['ema']=ta.ema(df['close'], length=10)
    return df


def main_strategy():
    print('Running main strategy...')
    p=ib.positions()
    pos=util.df(p)
    print(pos)

    for ticker in tickers:
        c=Crypto(ticker, 'PAXOS', 'USD')
        df=get_historical_data(c,'1 min','5 D')
        print(df)
        closing_price=df['close'].iloc[-1]
        current_supertrend=df['supertrend'].iloc[-1]
        prev_supertrend=df['supertrend'].iloc[-2]
        current_ema=df['ema'].iloc[-1]

        









while True:
    ct=pdlm.now(tz=time_zone2)
    print(ct)
    if ct.second==1 and ct.minute%time_frame1==0:
        main_strategy()

    #pnl check
    if ct.second%5==0:
        print('Checking PnL...')
        account_summary = ib.accountSummary()

        for item in account_summary:
            if item.tag == 'AvailableFunds':
                print(f"Available Balance: {item.value} {item.currency}")

    time.sleep(1)
    
