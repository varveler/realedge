from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .models import News
from .serializers import NewsSerializer

@api_view(['GET', ])
@authentication_classes((TokenAuthentication, ))
def news_list(request, ticker):
    if request.method == 'GET':
        news = News.objects.filter(tickers__contains=ticker)
        if news:
            many = True if news.count() > 1 else False
            serializer = NewsSerializer(news, many=many)
            return Response(serializer.data)
        return Response('Not Found', status=status.HTTP_404_NOT_FOUND)
    return Response('Method not allowed', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes((TokenAuthentication, ))
def news_detail(request, uuid):
    if request.method == 'GET':
        news = News.objects.get(uuid=uuid)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    return Response('Method not allowed', status=status.HTTP_400_BAD_REQUEST)
