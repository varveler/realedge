
from .mutils import (get_all_data,
                    give_trade_chart_start_and_end_dates,
                    give_gapper_chart_start_and_end_dates,
                    fix_data,
                    combine_data_filled_orders,
                    apply_vwap_pandas)
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from trades.models import Trade
from gappers.models import UpGapper

# Create your views here.
@api_view(['GET', ])
@authentication_classes((TokenAuthentication,))
def chart_data(request, uuid):
    print(uuid)
    if request.method == 'GET':
        trade = Trade.objects.get(uuid=uuid)
        start, end = give_trade_chart_start_and_end_dates(trade)
        data = get_all_data('1Min', trade.ticker, start, end)
        data = apply_vwap_pandas(data)
        fix_data(data)
        combine_data_filled_orders(data, trade)
        return Response(data)



@api_view(['GET', ])
@authentication_classes((TokenAuthentication,))
def gapper_data(request, slug):
    if request.method == 'GET':
        ticker = slug.split('-')[0]
        date = slug.split('-')[1]
        gapper = UpGapper.objects.filter(ticker=ticker, date__year=date[0:4], date__month=date[4:6], date__day=date[6:8])
        if not gapper:
            print('there is no gapper for', slug)
            return
        gapper = gapper[0]
        start, end = give_gapper_chart_start_and_end_dates(gapper)
        print(start, end, gapper.ticker)
        data = get_all_data('1Min', gapper.ticker, start, end)
        data = apply_vwap_pandas(data)
        fix_data(data)
        return Response(data)
