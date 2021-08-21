from common.utils import remove_zeros
from django.db.models import Sum

import datetime


def group_trades_by_ticker(trades):
    days = []
    format = '%Y-%m-%d'
    for trade in trades:
        if trade.start_time.date().strftime(format) not in days:
            days.append(trade.start_time.date().strftime(format))
    # group them together with a dict  like {'2021-04-30': {}, '2021-05-12': {}, '2021-05-13': {}}
    grouped_trades_by_day = {k: {} for k in days}
    for day in days:
        trades_day = trades.filter(start_time__year=day[0:4], start_time__month=day[5:7], start_time__day=day[8:10])
        grouped_trades_by_day[day] = trades_day
    for date, trades in grouped_trades_by_day.items():
        tickers = [] # get a list of tickers ['MOTH', 'AAPL', 'GME']
        [tickers.append(trade.ticker) for trade in trades if trade.ticker not in tickers]
        grouped_trades_by_ticker = {k: trades.filter(ticker=k) for k in tickers}
        # inser them in dict like {'2021-04-30': {'MOTH': queryset[trades...]}, '2021-05-12': {'AAPL': queryset[trades...]}, '2021-05-13': {'GME': queryset[trades...]}}
        grouped_trades_by_day[date] = grouped_trades_by_ticker
    # itereate over each day, each ticker to aggregata data and give final dictionary
    final_trades = []
    for date, ticker in grouped_trades_by_day.items():
        for ticker, trades in ticker.items():
            trades.order_by('-start_time')
            pnl = remove_zeros(trades.aggregate(Sum('pnl'))['pnl__sum'])
            shares_traded = str(trades.aggregate(Sum('max_size'))['max_size__sum'])
            #calculate if short, long or both
            sides = list(set([trade.side for trade in trades])) #['SH', 'SH','SH', 'LO'] to ['SH', 'LO']
            first = 'short' if sides[0] == 'SH' else 'long'
            side = 'both' if len(sides) > 1 else first
            calculated_comissions = remove_zeros(trades.aggregate(Sum('calculated_comissions'))['calculated_comissions__sum'])
            net = str(trades.aggregate(Sum('net'))['net__sum'])
            #serializer = DisplayTradeSerializer(trades, many=True)
            start_date = datetime.datetime.strftime(trades[0].start_time, '%b-%d-%Y').lower()
            small_uuid = str(trades[0].uuid).split('-')[0]
            slug = F'{ticker}-trades-by-{trades[0].user.user_name}-on-{start_date}-{small_uuid}'
            trade_info = {'trades_count': trades.count(),
                        'ticker': ticker,
                        'pnl': pnl,
                        'start_time': trades[0].start_time,
                        'date': date,
                        'side': side,
                        'calculated_comissions': calculated_comissions,
                        'net': net,
                        'shares_traded': shares_traded,
                        'trades_uuids': [trade.uuid for trade in trades],
                        'slug': slug,
                        #'trades': serializer.data,
                        }
            final_trades.append(trade_info)
            grouped_trades_by_day[date][ticker] = trade_info
    return final_trades
