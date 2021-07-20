from django.urls import path
from .views import trade_detail, orders_list, file_update, trades_list

urlpatterns = [
    path('detail/<slug>/', trade_detail),
    path('orders/', orders_list),
    path('upload/', file_update),
    path('trades/', trades_list),
]
