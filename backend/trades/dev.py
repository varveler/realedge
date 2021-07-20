
https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min



import pytz
import datetime

est = pytz.timezone('US/Eastern')
utc = pytz.utc


winter = datetime(2016, 1, 24, 18, 0, 0, tzinfo=utc)
summer = datetime(2016, 7, 24, 18, 0, 0, tzinfo=utc)

print winter.strftime(fmt)
print summer.strftime(fmt)

print winter.astimezone(est).strftime(fmt)
print summer.astimezone(est).strftime(fmt)

format = '%Y-%m-%dT%H:%M:%S-%Z'
time = "2021-04-07T13:34:00Z".replace('Z', '-UTC')
utc_dt = datetime.datetime.strptime(time, format)
utc_dt
est = pytz.timezone('US/Eastern')
est_dt = utc_dt.astimezone(est).strftime(format)
est_dt



string = "2021-04-07T13:30:00Z"
"transform incoming data from alpaca like 2021-04-07T13:34:00Z to dt object"
time = string.replace('Z', '-UTC')
format = '%Y-%m-%dT%H:%M:%S-%Z'
utc_dt = datetime.datetime.strptime(time, format)
est_dt = utc_dt.astimezone(US_EASTERN_TZ)
print(est_dt.strftime(format))
return est_dt

dates = [
    '2021-04-06T13:22:00Z',
    '2021-04-06T13:23:00Z',
    '2021-04-06T13:24:00Z',
    '2021-04-06T13:25:00Z',
    '2021-04-06T13:26:00Z',
    '2021-04-06T13:27:00Z',
    '2021-04-06T13:28:00Z',
    '2021-04-06T13:29:00Z',
    '2021-04-06T13:30:00Z',
    '2021-04-06T13:31:00Z',
    '2021-04-06T13:32:00Z',
    '2021-04-06T13:33:00Z',
    '2021-04-06T13:34:00Z',
    '2021-04-06T13:35:00Z',
    '2021-04-06T13:36:00Z',
    '2021-04-06T13:37:00Z',
    '2021-04-06T13:38:00Z',
    '2021-04-06T13:39:00Z',
    '2021-04-06T13:40:00Z',
    '2021-04-06T13:41:00Z',
]


for d in dates:
    convert_strUTC_to_aware_dt(d)






US_EASTERN_TZ = pytz.timezone('US/Eastern')
def convert_strUTC_to_aware_dt(string):
    "transform incoming data from alpaca like 2021-04-07T13:34:00Z to dt aware object"
    time = string.replace('Z', '-UTC')

    utc_dt = datetime.datetime.strptime(time, format)
    est_dt = utc_dt.astimezone(US_EASTERN_TZ)
    print(est_dt.strftime(format))
    return est_dt

et = convert_strUTC_to_aware_dt(time)

utc = pytz.utc
s = '2021-04-07T14:36:02Z'
s = s.replace('T', '-').replace('Z','').replace(':', '-')
l = [int(n) for n in s.split('-')]
l[4]
dt_utc = datetime.datetime(l[0], l[1], l[2], l[3], l[4], l[5], tzinfo=utc)
dt_utc
nt = dt_utc.astimezone(US_EASTERN_TZ)
dt_utc
nt



format = '%Y-%m-%dT%H:%M:%S-%Z'
US_EASTERN_TZ = pytz.timezone('US/Eastern')
utc = pytz.utc
def convert_str_to_est_dt(s,v):
    s = s.replace('T', '-').replace('Z','').replace(':', '-')
    l = [int(n) for n in s.split('-')]
    dt_utc = datetime.datetime(l[0], l[1], l[2], l[3], l[4], l[5], tzinfo=utc)
    dt_east = dt_utc.astimezone(US_EASTERN_TZ)
    #print(dt_east.strftime(format), v)
    return dt_east




import pytz
import datetime

est = pytz.timezone('US/Eastern')
utc = pytz.utc


winter = datetime(2016, 1, 24, 18, 0, 0, tzinfo=utc)
summer = datetime(2016, 7, 24, 18, 0, 0, tzinfo=utc)


def iex_convert_epoch_to_dt(timestamp):
    timestamp = int(str(timestamp)[:10])
    convertion = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(convertion)
    return convertion

import datetime

for t in dates:
    iex_convert_epoch_to_dt(t)



"""
import uuid

uuid.uuid4()
uuid.uuid4()
str(uuid.uuid4())

from yahooquery import Ticker
tickers = Ticker('fb')
tickers.history(period='5d', interval='1m')

t = Trade.objects.all()[0]
t

t.end_time
import datetime

'-'.join(str(t.uuid).split('-')[0:2])
str(self.uuid).split('-')[0:2].join('-')
abs(int(t.pnl))
t.slug


datetime.datetime.strftime(t.end_time, '%b-%d-%Y').lower()
p_or_l = 'proffit' if t.pnl > 0 else 'loss'
small_uuid = str(t.uuid).split('-')[0]
close_date = datetime.datetime.strftime(t.end_time, '%b-%d-%Y').lower()
'{ticker}-{pnl}-{p_or_l}-by-{username}-on-{close_date}-{small_uuid}'.format(ticker = t.ticker,
                                                                            pnl = abs(int(t.pnl)),
                                                                            p_or_l = p_or_l,
                                                                            username = t.user.user_name,
                                                                            close_date = close_date,
                                                                            small_uuid = small_uuid)

from django.db.models import Q
from .models import Order, Trade
from decimal import Decimal

def update_non_filled_orders_and_calculate_comissions():
    if object.closed:
        orders = Order.objects.filter(ticker=object.ticker).filter(Q( last_time__gte=object.start_time, start_time__lte=object.end_time) | Q(start_time__lte=object.end_time, last_time__gte=object.start_time)).exclude(status=Order.FILLED)
        for order in orders:
            order.trade = object
            order.save()
        filled_orders = object.order_set.filter(status=Order.FILLED)
        acumulator = 0
        for order in filled_orders:
            if order.type in [Order.MARKET or Order.STOP_MARKET]:
                if order.shares_executed < 200:
                    acumulator += Decimal(0.99)
                else:
                    acumulator += order.shares_executed * Decimal(0.005)
            else: #limit orders (or range?) latter review for range orders
                if order.shares_executed < 200:
                    acumulator += Decimal(0.99)
                else:
                    if order.start_time == order.last_time: #inmidiatly filled (not free)
                        acumulator += order.shares_executed * Decimal(0.005)
        instance.calculated_comissions = acumulator






trade = Trade.objects.filter(ticker='ISNS')
trade
trade = Trade.objects.get(pk=53)

trade
start = trade.start_time
end = trade.end_time
trade.ticker

Order.objects.filter(ticker=trade.ticker).filter(Q(last_time__gte=trade.start_time, start_time__lte=trade.end_time)|Q(start_time__lte=trade.end_time, last_time__gte=trade.start_time))
orders = Order.objects.filter(ticker=object.ticker).filter(Q( last_time__gte=object.start_time, start_time__lte=object.end_time) | Q(start_time__lte=object.end_time, last_time__gte=object.start_time)).exclude(status=Order.FILLED)
orders



from trades.models import OrdersFile
import pandas as pd
from trades.serializers import TZOrderSerializer
from django.contrib.auth.models import User
from celery.decorators import task
from common.utils import tradeZeroDateTimeString
from backend.settings.base import TIME_ZONE TIME_ZONE



local_file = OrdersFile.objects.all()[0]
user = User.objects.get(pk=1)
df = pd.read_excel(local_file._file)
df['sort_date'] = pd.to_datetime(df['Last Time'], format='%H:%M:%S %Y/%m/%d') # we use last time beause of limit orders
df['start_timedate_aware'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S %Y/%m/%d').dt.tz_localize('US/Eastern')
df['last_timedate_aware'] = pd.to_datetime(df['Last Time'], format='%H:%M:%S %Y/%m/%d').dt.tz_localize('US/Eastern')
df

import pytz
pytz.all_timezones

df = df.sort_values(by='sort_date')
df.fillna('', inplace=True)
for index, row in df.iterrows():
    serializer = TZOrderSerializer( data = {
        'ticker': row['Symbol/Contract'],
        'action' : row['Action'],
        'action_raw' : row['Action'],
        'shares': row['Shares'],
        'type' : row['Type'],
        'type_raw' : row['Type'],
        'route': row['Route'],
        'status' : row['Status'],
        'status_raw' : row['Status'],
        'shares_executed' : row['Executed'],
        'price' : row['AvgPrice'],
        'last_time' : row['last_timedate_aware'],
        'expiration' : row['Expiration'],
        'account' : row['Account'],
        'stop_price' : row['StopPrice'],
        'start_time' : row['start_timedate_aware'],
        'broker_info' : row['Text'],
        'limit_price' : row['LMT Price'],
        'broker' : 'TradeZero',
        'broker_ord_id': row['UserOrderID'],
        'user' : user.pk }
    )
    if serializer.is_valid():
        print('is valid')
        serializer.save()
    else: print(serializer.errors)
"""
