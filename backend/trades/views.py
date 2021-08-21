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
from .mutils import group_trades_by_ticker

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
@authentication_classes((TokenAuthentication, ))
def orders_list(request):
    if request.method == 'GET':
        uuids = request.query_params.getlist('trade[]')
        orders = Order.objects.filter(trade__uuid__in=uuids)
        many = True if orders.count() > 1 else False
        serializer = TZOrderSerializer(orders, many=many)
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


@api_view(['GET',])
@authentication_classes((TokenAuthentication,))
def grouped_trade_detail(request, slug):
    if request.method == 'GET':
        params = slug.split('-')
        ticker = params[0]
        user_name = params[3]
        d = datetime.datetime.strptime('-'.join(params[5:8]), '%b-%d-%Y')
        trades = Trade.objects.filter( ticker=ticker,
                                    #user=request.user,
                                    start_time__year=d.year,
                                    start_time__month=d.month,
                                    start_time__day=d.day)
        serializer = DisplayTradeSerializer(trades, many=True)
        details = group_trades_by_ticker(trades)
        return Response({'detailGroupedTrades': serializer.data, 'groupedDetails': details})


@api_view(['POST', ])
@authentication_classes((TokenAuthentication,))
def trade_comment(request, uuid):
    if request.method == 'POST':
        comment = request.data.get('comment', None)
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
        final_trades = group_trades_by_ticker(trades)
        return Response(final_trades)
    return Response("Method not allowed", status=status.HTTP_400_BAD_REQUEST)


def trade_detail_by_day_by_ticker(request):
    uuids = request.query_params.getlist('trade[]')

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
