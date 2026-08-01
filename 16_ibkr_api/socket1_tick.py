from ib_async import *

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=14)

# BTC/USD and ETH/USD via IBKR's Paxos crypto venue
btc = Crypto('BTC', 'PAXOS', 'USD')
eth = Crypto('ETH', 'PAXOS', 'USD')
ib.qualifyContracts(btc, eth)

ib.reqMktData(btc, '', False, False)
ib.reqMktData(eth, '', False, False)


def on_tick(tickers):

    for t in tickers:
        print(t.contract.symbol, t.time, 'bid:', t.bid, 'ask:', t.ask, 'last:', t.last, 'volume:', t.volume, 'high:', t.high, 'low:', t.low, 'close:', t.close)


ib.pendingTickersEvent += on_tick

ib.run()  # blocks here, streaming ticks until interrupted (Ctrl+C)


{Ticker(contract=Crypto(conId=479624278, symbol='BTC', exchange='PAXOS', currency='USD', localSymbol='BTC.USD', tradingClass='BTC'), time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), timestamp=1785068775.633558, minTick=0.25, bid=64515.0, bidSize=0.00305333, ask=64516.0, askSize=0.00305333, last=64504.75, lastSize=2.945e-05, lastTimestamp=datetime.datetime(2026, 7, 26, 12, 26, 12, tzinfo=datetime.timezone.utc), volume=88.0, high=64606.25, low=62000.0, close=64164.0, halted=0, ticks=[TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=1, price=64515.0, size=0.00305333), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=2, price=64516.0, size=0.00305333), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=4, price=64504.75, size=2.945e-05), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=5, price=64504.75, size=2.945e-05), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=8, price=-1, size=88.0), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=6, price=64606.25, size=0.0), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=7, price=62000.0, size=0.0), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=9, price=64164.0, size=0.0), TickData(time=datetime.datetime(2026, 7, 26, 12, 26, 15, 633548, tzinfo=datetime.timezone.utc), tickType=49, price=0, size=0)], defaults=IBDefaults(emptyPrice=-1, emptySize=0, unset=nan, timezone=datetime.timezone.utc), created=True)}


