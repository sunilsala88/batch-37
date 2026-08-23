from matplotlib import ticker
import pendulum as pdlm
import time
import logging
from  ib_async import *
from schedule import logger
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=18)

import indicators as ta




time_frame1=1
tickers = ['ETH','AAVE','BCH','LTC']

contract_objects={}
for ticker in tickers:
    c=ib.qualifyContracts(Crypto(ticker,'PAXOS', 'USD'))[0]
    print(c)
    contract_objects[ticker]=c
print(contract_objects)

time_zone= 'America/New_York'
# time_zone2= 'Asia/Kolkata'
account_no='DUH316001'

print(pdlm.now(tz=time_zone))




class PendulumFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = pdlm.from_timestamp(record.created, tz=time_zone)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.format('YYYY-MM-DD HH:mm:ss ZZ')


log_filename = f'strategy_{pdlm.now(tz=time_zone).to_date_string()}.log'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
handler.setLevel(logging.INFO)
handler.setFormatter(PendulumFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(PendulumFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

logger.info(f"Current time: {pdlm.now(tz=time_zone)} - Strategy started")




def get_info_about_position(pos,ticker_name):
     """ this function takes postion and ticker_name as input if i am long give 1,for short give -1, if no position or 0 quantity give 0"""
     #     #  c1=Stock(ticker_name, 'SMART', 'USD')
     c1=contract_objects.get(ticker_name)
     for p in pos:
         if p.contract.symbol == c1.symbol:
             if p.position > 0:
                 return 1
             elif p.position < 0:
                 return -1
             else:
                 return 0
     return 0

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

def check_market_order_placed(name):
    """Returns True if an open market order exists for the given ticker, False otherwise."""
    open_orders = ib.openOrders()
    for order in open_orders:
        if order.contract.symbol == name and order.orderType == 'MKT':
            return True
    return False


def trade_buy_crypto(ticker_name,quantity):
    if check_market_order_placed(ticker_name):
        logger.info(f'market order already placed for {ticker_name} so skipping placing new order')
        print(f'market order already placed for {ticker_name} so skipping placing new order')
        return 0
    logger.info(f'placing buy order for {ticker_name}')
    c1=contract_objects.get(ticker_name)
    order = MarketOrder('BUY', quantity, account=account_no)
    trade = ib.placeOrder(c1, order)
    logger.info(f'buy order placed for {ticker_name}')
    return trade

def strategy_condition(df,ticker,quantity):
    ema_now=df['ema'].iloc[-1]
    current_supertrend=df['supertrend'].iloc[-1]
    prev_supertrend=df['supertrend'].iloc[-2]
    closing_price=df['close'].iloc[-1]
    
    buy_condition=prev_supertrend<0 and current_supertrend>0 and ema_now<closing_price

    logger.info(f'Checking entry condition | {ticker} | ema={ema_now:.2f} supertrend={current_supertrend:.2f} | prev_supertrend={prev_supertrend:.2f} closing_price={closing_price:.2f}')
    if buy_condition:
        logger.info(f'BUY entry condition satisfied | {ticker} | qty={quantity}')
        trade_buy_crypto(ticker, quantity)
    else:
        # sell_condition when flat would open a naked short — skipped intentionally
        logger.info(f'No entry condition satisfied | {ticker}')
        return

def no_pending_market_order(name):
    """Return True if there is NO pending market order for this ticker, False if one exists."""
    ord=ib.openTrades()
    if ord:
        ord_df=util.df(ord)
        ord_df['name']=[c.symbol for c in ord_df['contract']]
        ord_df['ord_type']=[c.orderType for c in ord_df['order']]
        a=ord_df[(ord_df['name']==name) & (ord_df['ord_type']=='MKT')]
        if a.empty:
            return True
        else:
            return False
    else:
        return True

def close_ticker_position(name):
    # Guard: do not place another close if a market order is already pending
    if not no_pending_market_order(name):
        logger.info(f'Close order already pending for {name}, skipping')
        return
    try:
        pos=ib.positions(account=account_no)
        if not pos:
            logger.info(f'No positions found when trying to close {name}')
            return
        df2=util.df(pos)
        df2['ticker_name']=[cont.symbol for cont in df2['contract']]
        cont=contract_objects[name]
        filtered=df2[df2['ticker_name']==name]
        if filtered.empty:
            logger.info(f'No open position found for {name}, skipping close')
            return
        quant=filtered.position.iloc[0]
        logger.info(f'Closing position | {name} | qty={quant}')
        trade=None
        if quant>0:
            try:
                ord=Order(orderType='MKT',totalQuantity=int(abs(quant)),action='SELL',account=account_no,tif=ord_validity)
                trade=ib.placeOrder(cont,ord)
                logger.info(f'Close SELL order placed | {name} | qty={abs(quant)}')
            except Exception:
                logger.exception(f'Failed to place SELL close order for {name}')
        elif quant<0:
            try:
                ord=Order(orderType='MKT',totalQuantity=int(abs(quant)),action='BUY',account=account_no,tif=ord_validity)
                trade=ib.placeOrder(cont,ord)
                logger.info(f'Close BUY order placed | {name} | qty={abs(quant)}')
            except Exception:
                logger.exception(f'Failed to place BUY close order for {name}')
        # Wait for close order to fill
        if trade is not None:
            elapsed=0
            while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
                ib.sleep(1)
                elapsed+=1
            if trade.orderStatus.status=='Filled':
                logger.info(f'Close order filled | {name} | fill_price={trade.orderStatus.avgFillPrice}')
            else:
                logger.error(f'Close order NOT filled within timeout | {name} | status={trade.orderStatus.status}')
    except Exception:
        logger.exception(f'Unexpected error in close_ticker_position for {name}')


def main_strategy():
    print('Running main strategy...')



    for ticker in tickers:
        pos=ib.positions()
        c=contract_objects.get(ticker)
        df=get_historical_data(c,'1 min','5 D')
        print(df)
        current_price=df['close'].iloc[-1]
        current_supertrend=df['supertrend'].iloc[-1]
        prev_supertrend=df['supertrend'].iloc[-2]
        current_ema=df['ema'].iloc[-1]

        funds_list = [v for v in ib.accountValues(account=account_no) if v.tag == 'AvailableFunds']
        if not funds_list:
            logger.error(f'Could not retrieve AvailableFunds, skipping {ticker}')
            continue
        capital=int(float(funds_list[0].value))
        per_ticker_capital=capital/len(tickers)




        quantity=int(per_ticker_capital/current_price)
        position_status=get_info_about_position(pos,ticker)
        
        if quantity==0:
            print(f'Insufficient capital to trade {ticker}, skipping')
            logger.info(f'Insufficient capital to trade {ticker}, skipping')
            continue

        if position_status==0:
            print(f'No position in {ticker}, checking entry')
            logger.info(f'No position in {ticker}, checking entry')
            strategy_condition(df,ticker,quantity)

        elif position_status==1:
            print(f'Long position in {ticker}, checking exit')
            logger.info(f'Long position in {ticker}, checking exit')
            exit_condition=prev_supertrend>0 and current_supertrend<0 and current_ema>current_price
            if exit_condition:
                logger.info(f'EXIT condition satisfied for long {ticker}')
                close_ticker_position(ticker)
            else:
                logger.info(f'No exit condition for long {ticker}')

       








while True:
    ct=pdlm.now(tz=time_zone)
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
    
