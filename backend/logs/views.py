from rest_framework import permissions
from .models import TradesTickerLog, TradeTag
from .serializers import TradesTickerLogSerializer, TagsSerializer
from trades.models import DayTradesGroupedByDayByTicker
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    https://www.django-rest-framework.org/api-guide/permissions/
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TradesTickerLogDetail(APIView):
    """
    Retrieve, update or delete a trade Ticker log instance.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    #authentication_classes = [SessionAuthentication] to debug

    def get_object(self, ticker, date, user):
        try:
            obj = TradesTickerLog.objects.get(ticker=ticker, date=date, user=user)
            self.check_object_permissions(self.request, obj)
            return obj
        except TradesTickerLog.DoesNotExist:
            raise Http404

    def get_object_with_uuid(self, uuid):
        try:
            obj = TradesTickerLog.objects.get(uuid=uuid)
            self.check_object_permissions(self.request, obj)
            return obj
        except TradesTickerLog.DoesNotExist:
            raise Http404

    def get(self, request, ticker, date, *args, **kwargs):
        log = self.get_object(ticker, date, request.user.id)
        print('get', log)
        serializer = TradesTickerLogSerializer(log)
        return Response(serializer.data)

    def post(self, request, ticker, date):
        obj = TradesTickerLog.objects.filter(ticker=ticker, date=date, user=request.user.id)
        if obj.count() >= 1:
            return Response('Bad Request =(', status=status.HTTP_400_BAD_REQUEST)
        comments = request.data.get('comments', '')
        serializer = TradesTickerLogSerializer(data={'comments': comments,
                                                    'date': date,
                                                     'user': request.user.id,
                                                    'ticker':ticker})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, ticker, date):
        uuid = request.data.get('uuid', None)
        log = self.get_object_with_uuid(uuid)
        comments = request.data.get('comments', '')
        serializer = TradesTickerLogSerializer(log,
                                               data={'comments': comments},
                                               partial=True)
        if serializer.is_valid():
            serializer.save(comments=comments)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticker, date):
        uuid = request.data.get('uuid', None)
        print('delete uuid', uuid)
        log = self.get_object_with_uuid(uuid)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TradeAddRemoveTags(APIView):
    """
    Retrieve, update or delete a trade tags instance.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get_objects(self, ticker, date, user):
        #objs = TradeTag.objects.filter(ticker_date__ticker=ticker, ticker_date__date=date, ticker_date__user=user)
        objs = TradeTag.objects.filter(user=user)
        if objs.exists():
            self.check_object_permissions(self.request, objs[0])
            return objs
        raise Http404

    def get(self, request, ticker, date, *args, **kwargs):
        tags = self.get_objects(ticker, date, request.user.id)
        serializer = TagsSerializer(tags, many = True, context={'ticker': ticker, 'date':  date})
        return Response(serializer.data)

    def post(self, request, ticker, date, *args, **kwargs):
        """ Creates a new tag and creates the relationship for that trade """
        day_trades = DayTradesGroupedByDayByTicker.objects.filter(ticker=ticker, date=date, user=request.user)
        if not day_trades.exists() or day_trades.count() > 1:
            return Response('Bad Request No trades on that day with given ticker =( ', status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('name', '')
        type = request.data.get('type', 'NE')
        tag = TradeTag.objects.create(name=name, type=type, user=request.user)
        tag.ticker_date.add(day_trades.get())
        serializer = TagsSerializer(tag)
        return Response(serializer.data)

    def put(self, request, ticker, date, *args, **kwargs):
        """ Creates a new relationship for that trade in an existing tag """
        day_trades = DayTradesGroupedByDayByTicker.objects.filter(ticker=ticker, date=date, user=request.user)
        if not day_trades.exists() or day_trades.count() > 1:
            return Response('Bad Request No trades on that day with given ticker =( ', status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('name', '')
        type = request.data.get('type', '')
        print('################', name, type, request.user)
        tag = TradeTag.objects.get(name=name, type=type, user=request.user)
        self.check_object_permissions(self.request, tag)
        tag.ticker_date.add(day_trades.get())
        serializer = TagsSerializer(tag)
        return Response(serializer.data)

    def delete(self, request, ticker, date, *args, **kwargs):
        """ Deletes the relationship between a tag an Grouped Day Trades """
        day_trades = DayTradesGroupedByDayByTicker.objects.filter(ticker=ticker, date=date, user=request.user)
        if not day_trades.exists() or day_trades.count() > 1:
            return Response('Bad Request No trades on that day with given ticker =( ', status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('name', '')
        type = request.data.get('type', '')
        print('################', name, type, request.user)
        tag = get_object_or_404(TradeTag, name=name, type=type, user=request.user)
        self.check_object_permissions(self.request, tag)
        serializer = TagsSerializer(tag)
        tag.ticker_date.remove(day_trades.get())
        return Response(serializer.data)
