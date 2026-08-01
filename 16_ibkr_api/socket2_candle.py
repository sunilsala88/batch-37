from ib_async import *

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=15)

# BTC/USD via IBKR's Paxos crypto venue
btc = Crypto('BTC', 'PAXOS', 'USD')
ib.qualifyContracts(btc)

# 5-second realtime bars, streamed over the same socket connection until cancelled
bars = ib.reqRealTimeBars(btc, barSize=5, whatToShow='MIDPOINT', useRTH=False)


def on_bar_update(bars, hasNewBar):
    if hasNewBar:
        bar = bars[-1]
        print(bar.time, 'open:', bar.open_, 'high:', bar.high, 'low:', bar.low, 'close:', bar.close, 'volume:', bar.volume)


bars.updateEvent += on_bar_update

ib.run()  # blocks here, streaming candles until interrupted (Ctrl+C)
