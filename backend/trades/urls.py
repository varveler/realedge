from django.urls import path
from .views import orders_list, file_update, trades_list

urlpatterns = [
    path('orders/', orders_list),
    path('upload/', file_update),
    path('trades/', trades_list),
]
