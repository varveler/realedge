import requests
import datetime
import pytz
import pandas as pd
import numpy as np
from backend.settings.base import get_env_variable
from trades.models import Order, Trade
from common.utils import atr


APCA_API_SECRET_KEY = get_env_variable('APCA_API_SECRET_KEY')
APCA_API_KEY_ID = get_env_variable('APCA_API_KEY_ID')
US_EASTERN_TZ = pytz.timezone('US/Eastern')
utc = pytz.utc


def get_all_data(timeframe, ticker, start, end, page_token=None, bars=[]):
    if datetime.datetime == type(start):
        start = datetime.datetime.strftime( start, '%Y-%m-%dT%H:%M:%SZ')
    if datetime.datetime == type(end):
        end = datetime.datetime.strftime( end, '%Y-%m-%dT%H:%M:%SZ')
    url = 'https://data.alpaca.markets/v2/stocks/{ticker}/bars'.format(ticker=ticker)
    query_params = {'timeframe': timeframe, 'start': start, 'end': end, 'page_token': page_token}
    headers = {'APCA-API-KEY-ID': APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}
    response = requests.get(url, headers=headers, params=query_params)
    data = response.json()
    bars = bars + data['bars']
    token = data['next_page_token']
    if not token:
        return bars
    return get_all_data(timeframe, ticker, start, end, page_token=token, bars=bars)


def give_trade_chart_start_and_end_dates(trade):
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


def give_gapper_chart_start_and_end_dates(gapper):
    gdate = gapper.date
    trading_hours_trade_end_time = datetime.datetime(gdate.year, gdate.month, gdate.day, 3, 31, 0, tzinfo=US_EASTERN_TZ)
    if gdate.weekday() == 0: #is monday
        days = 3
    else:
        days = 1
    end_of_prev_day_est = trading_hours_trade_end_time - datetime.timedelta(days=days)
    end_of_prev_day_utc = end_of_prev_day_est.astimezone(utc)
    end_of_day_est = datetime.datetime(gdate.year, gdate.month, gdate.day, 23, 59, 59, tzinfo=US_EASTERN_TZ)
    end_of_day_utc = end_of_day_est.astimezone(utc)
    return end_of_prev_day_utc, end_of_day_utc

def fix_data(data):
    for candle in data:
        candle['open'] = candle.pop('o')
        candle['close'] = candle.pop('c')
        candle['high'] = candle.pop('h')
        candle['low'] = candle.pop('l')
        candle['date'] = candle.pop('t')
        candle['volume'] = candle.pop('v')
        candle['entryShort'] = None
        candle['entryLong'] = None
        candle['exitShort'] = None
        candle['exitLong'] = None
        candle['executionPrice'] = None
    return data


def give_triangle_distance(data, index, n=14, factor=1):
    """
        trims and converts a list of dictionaries to pandas dataframe then
        caluclate the last atr used for the chart feature to give extra space
        on entry triangles
    """

    data = data[index - (n + 1) : index]
    df = pd.DataFrame(data)
    return atr(df, n=n).get(n) * factor

#entry orders
def combine_data_filled_orders(data, parent_trade, orders):
    """
        fills missing data on chart data like orders executionPrice
        and triangle markers: entryShort, entryLong, exitShort, exitLong
    """
    filled_orders = orders.filter(status='FI')
    format = '%Y-%m-%dT%H:%M:00Z'
    for i, candle in enumerate(data):
        for order in filled_orders:
            order_date = datetime.datetime.strftime(order.last_time, format)
            if candle['date'] == order_date:
                extra_distance = give_triangle_distance(data, i)
                if parent_trade.side == Trade.SHORT:
                    if order.in_out == Order.InOut.IN: #entry short
                        candle['entryShort'] = candle['high'] + extra_distance
                    elif order.in_out == Order.InOut.OUT: #exit short
                        candle['exitShort'] = candle['low'] - extra_distance
                elif parent_trade.side == Trade.LONG:
                    if order.in_out == Order.InOut.IN: #entry long
                        candle['entryLong'] = candle['low'] - extra_distance
                    elif order.in_out == Order.InOut.OUT: #exit long
                        candle['exitLong'] = candle['high'] + extra_distance
                candle['executionPrice'] = order.price

"""
def apply_vwap_pandas(data):
    df = pd.DataFrame(data)
    df['vwap_pandas'] = (df.v * (df.h + df.l) / 2).cumsum() / df.v.cumsum()
    return df.to_dict('records')
"""

def apply_vwap_pandas(data):
    df = pd.DataFrame(data)
    df['dt'] = pd.to_datetime(df['t']).copy()
    df['EST'] = df['dt'].dt.tz_convert('US/Eastern').copy()
    dfg = df.groupby([df['EST'].dt.date])
    if len(dfg) > 1:
        vwap = dfg.apply(lambda df: (df.v*(df.h + df.l)/2).cumsum() / df.v.cumsum()) #df['vwap_pandas'] = (df.v*(df.h + df.l)/2).cumsum() / df.v.cumsum()p
        vwap.reset_index()
        df = dfg.obj
        df['vwap_pandas'] = vwap.reset_index()[0]
        return df.to_dict('records')
    else:
        df['vwap_pandas'] = (df.v*(df.h+df.l)/2).cumsum() / df.v.cumsum()
        return df.to_dict('records')


def apply_intraday_vwap_pandas(data):
    df = pd.DataFrame(data)
    df['dt'] = pd.to_datetime(df['t']).copy()
    df['EST'] = df['dt'].dt.tz_convert('US/Eastern').copy()
    df['EST_index'] = df['EST'].copy()
    df = df.set_index('EST_index')
    gdf = df.between_time('9:30', '16:00').copy()
    ggdf = gdf.groupby([gdf['EST'].dt.date])
    if len(ggdf) > 1:
        vwap = ggdf.apply(lambda df: (df.v * (df.h + df.l) / 2).cumsum() / df.v.cumsum())
        vwap.name = 'intradayVwap'
        vwap = pd.DataFrame(vwap)
        vwap = vwap.reset_index(level=0, drop=True)
    else:
        gdf['intradayVwap'] = (gdf.v * (gdf.h + gdf.l) / 2).cumsum() / gdf.v.cumsum()
        vwap = pd.DataFrame(gdf['intradayVwap'])
    df = df.join(vwap)
    df.intradayVwap = df.intradayVwap.fillna('')
    return df.reset_index().to_dict('records')
