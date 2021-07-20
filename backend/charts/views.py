
from .mutils import get_all_data, give_chart_start_and_end_dates, fix_data, combine_data_filled_orders
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from trades.models import Trade

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
