from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import UpGapper
from .serializers import GapperSerializer, PublicGapperSerializer
from common.utils import convert_str_to_dateobj

import datetime
from django.utils import timezone

# Create your views here.
def homepage(request):
    return render(request, '_next/out/index.html')


@csrf_exempt
def public_gappers(request):
    if request.method == 'GET':
        param = request.GET.get('oldest', None)
        EXTRA_DAYS = 15
        gappers = None
        now = timezone.now().date()
        while not gappers:
            if param:
                oldest = convert_str_to_dateobj(param)
                extra = oldest - datetime.timedelta(days=EXTRA_DAYS)
            else:
                extra = now - datetime.timedelta(days=EXTRA_DAYS)
            gappers = UpGapper.objects.filter(date__gte=extra, gap_percentage__gte=0.2)
            EXTRA_DAYS =+ 1
        serializer = PublicGapperSerializer(gappers, many=True, )
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def loged_in_gappers(request):
    if request.method == 'GET':
        param = request.GET.get('oldest', None)
        EXTRA_DAYS = 15
        if param:
            oldest = convert_str_to_dateobj(param)
            extra = oldest - datetime.timedelta(days=EXTRA_DAYS)
        else:
            now = timezone.now().date()
            extra = now - datetime.timedelta(days=EXTRA_DAYS)
        gappers = UpGapper.objects.filter(date__gte=extra)
        serializer = GapperSerializer(gappers, many=True, )
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', ])
def gapper_detail(request, _id):
    ticker = _id.split('-')[0]
    date = _id.split('-')[1]
    gapper = UpGapper.objects.filter(ticker=ticker, date__year=date[0:4], date__month=date[4:6], date__day=date[6:8])
    if gapper:
        gapper = gapper[0]
        serializer = GapperSerializer(gapper)
        return JsonResponse(serializer.data)
    return Response([], status=status.HTTP_404_NOT_FOUND)
