from django.urls import path
from .views import TradesTickerLogDetail, TradeAddRemoveTags
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('<str:ticker>/<str:date>/', csrf_exempt(TradesTickerLogDetail.as_view())),
    path('tags/<str:ticker>/<str:date>/', csrf_exempt(TradeAddRemoveTags.as_view()))

]
