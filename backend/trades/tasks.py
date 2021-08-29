
from trades.models import OrdersFile
import pandas as pd
from trades.serializers import TZOrderSerializer
from celery.decorators import task
from backend.settings.base import TIME_ZONE
from reusers.models import ReUser as User

@task(name='process_orders_from_file_TradeZero')
def process_orders_from_file_TradeZero(pk, user_pk):
    """
    Gives the orders a chronological Order to save to db
    """
    order_file = OrdersFile.objects.get(pk=pk)
    user = User.objects.get(pk=user_pk)
    df = pd.read_excel(order_file._file)
    df['sort_date'] = pd.to_datetime(df['Last Time'], format='%H:%M:%S %Y/%m/%d') # we use last time beause of limit orders
    df['start_timedate_aware'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S %Y/%m/%d').dt.tz_localize(TIME_ZONE)
    df['last_timedate_aware'] = pd.to_datetime(df['Last Time'], format='%H:%M:%S %Y/%m/%d').dt.tz_localize(TIME_ZONE)
    df = df.sort_values(by='sort_date')
    df.fillna('', inplace=True)
    for index, row in df.iterrows():
        print(row['AvgPrice'], row['Executed'] )
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
            'user' : user.pk
            }
        )
        if serializer.is_valid():
            serializer.save()
    order_file.delete()
