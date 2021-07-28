from charts.mutils import get_all_data, give_trade_chart_start_and_end_dates, give_gapper_chart_start_and_end_dates, fix_data, combine_data_filled_orders
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from trades.models import Trade
import pandas as pd
# Create your views here.
@api_view(['GET', ])
@authentication_classes((TokenAuthentication,))
def chart_data(request, uuid):
    if request.method == 'GET':
        trade = Trade.objects.get(uuid=uuid)
        start, end = give_chart_start_and_end_dates(trade)
        data = get_all_data('1Min', trade.ticker, start, end)
        fixed_data = fix_data(data)
        combined_data = combine_data_filled_orders(data, trade)
        return Response(fixed_data)




def apply_vwap_pandas(data):
    df = pd.DataFrame(data)
    df['vwap_pandas'] = (df.v*(df.h+df.l)/2).cumsum() / df.v.cumsum()
    return df.to_dict('records')



trade = Trade.objects.get(uuid='f0766c31-e97d-4c43-abb9-c358b5bc8e39')
start, end = give_trade_chart_start_and_end_dates(trade)
data = get_all_data('1Min', trade.ticker, start, end)
df = pd.DataFrame(data)
df['dt'] = pd.to_datetime(df['t'])
df['EST'] = df['dt'].dt.tz_convert('US/Central')
dfg = df.groupby([df['EST'].dt.date])
vwap = dfg.apply(lambda df: (df.v*(df.h + df.l)/2).cumsum() / df.v.cumsum()) #df['vwap_pandas'] = (df.v*(df.h + df.l)/2).cumsum() / df.v.cumsum()
vwap.reset_index()
df = dfg.obj
df['vwap'] =  vwap.reset_index()[0]
df.to_dict('records')

"""

Get trade inital date
To render intraday charts:
    determine days necesary for send data: [day-1, day0,]
        -available day0 data:
            is eod data available?
            yes: return that data else query for available data, do not save it
        -previuos days data
            is eod previus day data avialable?
            yes: return that data else query for available data, save it as a DAY FILE json and return it
To render day charts:
    determine days necesary for send data: [days-45, days+5]
    is data available?
    yes return it else query it save it and return it

data = [{'t': "2021-05-12T12:29:00Z", 'o': 5.01, 'h': 5.01, 'l': 5.01, 'c': 5.01, 'v': 50},
        {'t': "2021-05-12T13:30:00Z", 'o': 5.15, 'h': 5.15, 'l': 5.15, 'c': 5.15, 'v': 50},
        {'t': "2021-05-12T13:32:00Z", 'o': 5.1395, 'h': 5.1395, 'l': 5.1395, 'c': 5.1395, 'v': 50},
        {'t': "2021-05-12T13:33:00Z", 'o': 5.23, 'h': 5.23, 'l': 5.23, 'c': 5.23, 'v': 50},
        {'t': "2021-05-12T13:37:00Z", 'o': 5.29, 'h': 5.29, 'l': 5.29, 'c': 5.29, 'v': 50},
        {'t': "2021-05-12T13:38:00Z", 'o': 5.29, 'h': 5.45, 'l': 5.23, 'c': 5.38, 'v': 50},
        {'t': "2021-05-12T13:39:00Z", 'o': 5.37, 'h': 5.37, 'l': 5.31, 'c': 5.31, 'v': 50}]


fix_data(data)




def fix_data(data):
    for candle in data:
        candle['open'] = candle.pop('o')
        candle['close'] = candle.pop('c')
        candle['high'] = candle.pop('h')
        candle['low'] = candle.pop('l')
        candle['date'] = candle.pop('t')
        candle['volume'] = candle.pop('v')
    return data












from django.utils import timezone
import pytz
utc = pytz.utc
US_EASTERN_TZ = pytz.timezone('US/Eastern')
trade = Trade.objects.all()[0]
trade.uuid

tend = trade.end_time
end_time_est = tend.astimezone(US_EASTERN_TZ)
end_of_day_est = datetime.datetime(end_time_est.year, end_time_est.month, end_time_est.day, 23, 59, 59, tzinfo=US_EASTERN_TZ)
end_of_day_utc = end_of_day_est.astimezone(utc)

tstart = trade.start_time
tstart
start_time_est = tstart.astimezone(US_EASTERN_TZ)
start_time_est
trading_hours_trade_end_time = datetime.datetime(start_time_est.year, start_time_est.month, start_time_est.day, 3, 31, 0, tzinfo=US_EASTERN_TZ)
if start_time_est.weekday() == 0: #is monday
    days = 3
else:
    days = 1
end_of_prev_day_est = trading_hours_trade_end_time - datetime.timedelta(days=days)
end_of_prev_day_utc = end_of_prev_day_est.astimezone(utc)








utc = pytz.utc
US_EASTERN_TZ = pytz.timezone('US/Eastern')
def give_chart_start_and_end_dates(trade):
    tstart = trade.start_time
    start_time_est = tstart.astimezone(US_EASTERN_TZ)
    trading_hours_trade_end_time = datetime.datetime(start_time_est.year, start_time_est.month, start_time_est.day, 3, 31, 0, tzinfo=US_EASTERN_TZ)
    if start_time_est.weekday() == 0: #is monday
        days = 3
    else:
        days = 1
    end_of_prev_day_est = trading_hours_trade_end_time - datetime.timedelta(days=days)
    end_of_prev_day_utc = end_of_prev_day_est.astimezone(utc)
    tend = trade.end_time
    end_time_est = tend.astimezone(US_EASTERN_TZ)
    end_of_day_est = datetime.datetime(end_time_est.year, end_time_est.month, end_time_est.day, 23, 59, 59, tzinfo=US_EASTERN_TZ)
    end_of_day_utc = end_of_day_est.astimezone(utc)
    return end_of_prev_day_utc, end_of_day_utc







import requests
import datetime
from backend.settings.base import get_env_variable



APCA_API_SECRET_KEY = get_env_variable('APCA_API_SECRET_KEY')
def get_all_data(timeframe, ticker, start, end, page_token=None, bars=[]):
    if datetime.datetime == type(start):
        start = datetime.datetime.strftime( start, '%Y-%m-%dT%H:%M:%SZ')
    if datetime.datetime == type(end):
        end = datetime.datetime.strftime( end, '%Y-%m-%dT%H:%M:%SZ')
    url = 'https://data.alpaca.markets/v2/stocks/{ticker}/bars'.format(ticker=ticker)
    query_params = {'timeframe': timeframe, 'start': start, 'end': end, 'page_token': page_token}
    headers = {'APCA-API-KEY-ID': 'PKGQJAO34FE1231S5GBR', 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}
    response = requests.get(url, headers=headers, params=query_params)
    data = response.json()
    bars = bars + data['bars']
    token = data['next_page_token']
    if not token:
        return bars
    return get_all_data(timeframe, ticker, start, end, page_token=token, bars=bars)




def convert_str_to_est_dt(s):
    s = s.replace('T', '-').replace('Z','').replace(':', '-')
    l = [int(n) for n in s.split('-')]
    dt_utc = datetime.datetime(l[0], l[1], l[2], l[3], l[4], l[5], tzinfo=utc)
    dt_east = dt_utc.astimezone(US_EASTERN_TZ)
    #print(dt_east.strftime(format), v)
    return dt_east

format = '%Y-%m-%dT%H:%M:%S-%Z'
US_EASTERN_TZ = pytz.timezone('US/Eastern')
utc = pytz.utc
import requests
ticker = 'DARE'
url = 'https://data.alpaca.markets/v2/stocks/{ticker}/bars'.format(ticker=ticker)
#AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min'
query = {'timeframe':'1Min', 'start':'2021-07-05T09:01:00Z', 'end':'2021-07-08T22:01:00Z', 'next_page':None}
headers={'APCA-API-KEY-ID':'PKGQJAO34FE1231S5GBR', 'APCA-API-SECRET-KEY':'y1civhZNLL0I6cYAjoPn0S4xyZmAbw1ThBCgOU9s'}
response = requests.get(url, headers=headers, params=query)
bars = response.json()['bars']
token = response.json()['next_page_token']
query['page_token'] = token
query
response.json()

response2 = requests.get(url, headers=headers, params=query)

response2
response2.json()
response2.json()

t = Trade.objects.all()[0]
t
start = t.start_time
t.end_time

datetime.datetime == type(start)
datetime.datetime.strftime( start, '%Y-%m-%dT%H:%M:%SZ')


'start':'2021-07-05T09:01:00Z', 'end':'2021-07-08T22:01:00Z'
start = datetime.datetime(2021, 7, 5, 9, 1, 00)
end = datetime.datetime(2021, 7, 8, 22, 1, 00)
start
end
datetime.datetime.strftime( start, '%Y-%m-%dT%H:%M:%SZ')
datetime.datetime.strftime( end, '%Y-%m-%dT%H:%M:%SZ')
def get_all_data(timeframe, ticker, start, end, page_token=None, bars=[]):
    #_file = StockBarDataFile.filter(ticker=ticker, start__gte=start)
    # if not file:
    if datetime.datetime == type(start):
        start = datetime.datetime.strftime( start, '%Y-%m-%dT%H:%M:%SZ')
    if datetime.datetime == type(end):
        end = datetime.datetime.strftime( end, '%Y-%m-%dT%H:%M:%SZ')
    url = 'https://data.alpaca.markets/v2/stocks/{ticker}/bars'.format(ticker=ticker)
    query_params = {'timeframe': timeframe, 'start': start, 'end': end, 'page_token': page_token}
    headers = {'APCA-API-KEY-ID': 'PKGQJAO34FE1231S5GBR', 'APCA-API-SECRET-KEY': 'y1civhZNLL0I6cYAjoPn0S4xyZmAbw1ThBCgOU9s'}
    response = requests.get(url, headers=headers, params=query_params)
    data = response.json()
    bars = bars + data['bars']
    token = data['next_page_token']
    if not token:
        return bars
    return get_all_data(timeframe, ticker, start, end, page_token=token, bars=bars)


data3 = get_all_data('1Min', 'DARE', start, end)
len(data3)

for i, d in enumerate(data3):
    print(i, d['t'], d['v'])

"""
