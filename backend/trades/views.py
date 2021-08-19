from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Order, Trade, OrdersFile
from .serializers import TZOrderSerializer, DisplayTradeSerializer
from .forms import OrdersFileForm
from .tasks import process_orders_from_file_TradeZero
from common.utils import DecimalEncoder, remove_zeros
from django.db.models import Sum

import datetime
import json

class OrdersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view Orders.
    """
    queryset = Order.objects.all().order_by('-last_time')
    serializer_class = TZOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def orders_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = TZOrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TZOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        print(3)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def file_update(request):
    user = request.user
    form = OrdersFileForm()
    context = {'form': form}
    if request.method == 'POST':
        form = OrdersFileForm(request.POST)
        local_file = request.FILES.get('local_file', None)
        if local_file:
            l_file = OrdersFile(_file=local_file, user=user)
            l_file.save()
            process_orders_from_file_TradeZero.delay(l_file.pk, user.pk)
    return render(request, 'trades/upload_file.html', context)



@api_view(['GET', ])
@authentication_classes((TokenAuthentication,))
def trades_list(request):
    if request.method == 'GET':
        trades = Trade.objects.all().order_by('-creation')
        serializer = DisplayTradeSerializer(trades, many=True)
        return Response(serializer.data)


@api_view(['GET',])
@authentication_classes((TokenAuthentication,))
def trade_detail(request, slug):
    if request.method == 'GET':
        trade = Trade.objects.get(closed_slug=slug)
        serializer = DisplayTradeSerializer(trade)
        return Response(serializer.data)



@api_view(['POST', ])
@authentication_classes((TokenAuthentication,))
def trade_comment(request, uuid):
    if request.method == 'POST':
        print('post on trade ', uuid)
        comment = request.data.get('comment', None)
        print('comment ', comment)
        trade = Trade.objects.get(uuid=uuid)
        trade_serialized = DisplayTradeSerializer(trade,
                                                data={'comments': comment},
                                                partial=True)
        if trade_serialized.is_valid():
            trade_serialized.save()
            return Response(trade_serialized.data, status=status.HTTP_202_ACCEPTED)
    return Response("Method not allowed", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes((TokenAuthentication,))
def grouped_trades_by_day_by_ticker(request):
    if request.method == 'GET':
        trades = Trade.objects.all().order_by('-creation')
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
                serializer = DisplayTradeSerializer(trades, many=True)
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

        #json_response = json.dumps(grouped_trades_by_day, cls=DecimalEncoder)
        return Response(final_trades)
    return Response("Method not allowed", status=status.HTTP_400_BAD_REQUEST)



#from operator import itemgetter
#from itertools import groupby


# @authentication_classes((TokenAuthentication,))
# @api_view(['GET', ])
# def grouped_trades_by_day_by_ticker2(request):
#     if request.method == 'GET':
#         trades = Trade.objects.all().order_by('-creation')
#         key = itemgetter('date')
#         iter = groupby(trades, key=key) # assuming queryset is already sorted by city_name
#         for key, group in iter:
#             print(key)
#             key2 = itemgetter('ticker')
#             iter2 = groupby(sorted(group, key=key2), key=key2) # now we must sort by company_name
#             for comp, branch in iter2:
#                 print(comp)
#                 for b in branch:
#                     print(b)
