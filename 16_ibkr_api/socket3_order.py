from ib_async import *

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=77)

# BTC/USD via IBKR's Paxos crypto venue
btc = Crypto('BTC', 'PAXOS', 'USD')
ib.qualifyContracts(btc)

# limit order placed well away from market so it stays open and lets us watch status changes
order = LimitOrder('BUY', 0.001, 50000)
trade = ib.placeOrder(btc, order)


def on_order_status(trade):
    o = trade.order
    s = trade.orderStatus
    print(o.orderId, o.action, o.totalQuantity, trade.contract.symbol,
          'status:', s.status, 'filled:', s.filled, 'remaining:', s.remaining, 'avgFillPrice:', s.avgFillPrice)


ib.orderStatusEvent += on_order_status

ib.run()  # blocks here, streaming order status updates until interrupted (Ctrl+C)
