from rest_framework import permissions
from .models import TradesTickerLog
from .serializers import TradesTickerLogSerializer
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication



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
        print('post', obj)
        if obj.count() >= 1:
            print('post + 1', obj)
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
