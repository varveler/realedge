from django.urls import path, re_path
from .views import trade_data, gapper_data

urlpatterns = [
    path('trade/<str:time_frame>/', trade_data),
    path('gapper/<str:time_frame>/<str:slug>/', gapper_data),
]
