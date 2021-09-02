from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import News
from .serializers import NewsSerializer
from common.utils import get_start_end_dates


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def news_list(request, ticker):
    if request.method == 'GET':
        _from = request.GET.get('from', None)
        to = request.GET.get('to', None)
        print('########## # # #ticker from to ####### # # #', ticker, _from, to)
        start, end = get_start_end_dates(_from, to)
        news = News.objects.filter(tickers__contains=ticker,
            publish_date__lte=end,
            publish_date__gte=start)
        if news.exists():
            many = True if news.count() > 1 else False
            serializer = NewsSerializer(news, many=many)
            return Response(serializer.data)
        return Response('No news Found', status=status.HTTP_404_NOT_FOUND)
    return Response('Method not allowed', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def news_detail(request, uuid):
    if request.method == 'GET':
        news = News.objects.get(uuid=uuid)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    return Response('Method not allowed', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def partialnews_list(request, ticker):
    if request.method == 'GET':
        _from = request.GET.get('from', None)
        to = request.GET.get('to', None)
        print('########## # # #ticker from to ####### # # #', ticker, _from, to)
        start, end = get_start_end_dates(_from, to)
        news = News.objects.filter(tickers__contains=ticker,
            internal_source='scraping Finviz',
            publish_date__lte=end,
            publish_date__gte=start).order_by('title', 'publish_date').distinct('title')
        if news.exists():
            many = True if news.count() > 1 else False
            serializer = NewsSerializer(news, many=many)
            return Response(serializer.data)
        return Response('No news Found', status=status.HTTP_404_NOT_FOUND)
    return Response('Method not allowed', status=status.HTTP_400_BAD_REQUEST)
