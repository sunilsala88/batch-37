from ib_async import IB

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

account_summary = ib.accountSummary()

for item in account_summary:
    if item.tag == 'AvailableFunds':
        print(f"Available Balance: {item.value} {item.currency}")

ib.disconnect()
