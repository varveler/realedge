

"""
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
from backend.settings.base import TIME_ZONE
TIME_ZONE



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
