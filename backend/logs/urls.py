from django.urls import path
from .views import TradesTickerLogDetail
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('<str:ticker>/<str:date>/', csrf_exempt(TradesTickerLogDetail.as_view()))

]
