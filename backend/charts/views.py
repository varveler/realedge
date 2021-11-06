
from .mutils import (get_all_data,
                    give_trade_chart_start_and_end_dates,
                    give_gapper_chart_start_and_end_dates,
                    fix_data,
                    combine_data_filled_orders,
                    apply_vwap_pandas,
                    apply_intraday_vwap_pandas,
                    combine_data_with_news,
                    remove_na)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from trades.models import Trade, Order
from gappers.models import UpGapper
from news.models import News
from django.http import JsonResponse
from pprint import pprint
#from .data import data
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def trade_data(request, time_frame):
    if request.method == 'GET':
        uuids = request.query_params.getlist('trade[]')
        print(time_frame)
        trades = Trade.objects.filter(uuid__in=uuids)
        print(trades)
        orders = Order.objects.filter(trade__uuid__in=uuids)
        ticker = trades.first().ticker
        start, end = give_trade_chart_start_and_end_dates(trades[0], time_frame)
        data = get_all_data(time_frame, ticker, start, end)
        data = apply_vwap_pandas(data)
        data = apply_intraday_vwap_pandas(data)
        data = remove_na(data)
        fix_data(data)
        combine_data_filled_orders(data, trades[0], orders)
        news = News.objects.filter(tickers__contains=ticker, publish_date__lte=end, publish_date__gte=start)
        combine_data_with_news(data, news)
        return Response(data)


@api_view(['GET', ])
def gapper_data(request, slug, time_frame):
    if request.method == 'GET':
        ticker = slug.split('-')[0]
        date = slug.split('-')[1]
        gapper = UpGapper.objects.filter(ticker=ticker, date__year=date[0:4], date__month=date[4:6], date__day=date[6:8])
        if not gapper:
            print('not gapper')
            return
        gapper = gapper[0]
        start, end = give_gapper_chart_start_and_end_dates(gapper, time_frame)
        data = get_all_data(time_frame, gapper.ticker, start, end)
        data = apply_vwap_pandas(data)
        data = apply_intraday_vwap_pandas(data)
        data = remove_na(data)
        fix_data(data)
        news = News.objects.filter(tickers__contains=ticker, publish_date__lte=end, publish_date__gte=start)
        combine_data_with_news(data, news)
        return Response(data)
