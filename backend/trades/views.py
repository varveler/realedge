from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Order, Trade, OrdersFile
from .serializers import TZOrderSerializer, DisplayTradeSerializer
from .forms import OrdersFileForm
from .tasks import process_orders_from_file_TradeZero

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
@permission_classes((IsAuthenticated, ))
def trades_list(request):
    if request.method == 'GET':
        trades = Trade.objects.all().order_by('-creation')
        serializer = DisplayTradeSerializer(trades, many=True)
        return Response(serializer.data)
