from django.urls import path
from .views import trade_detail, orders_list, file_update, trades_list, trade_comment

urlpatterns = [
    path('detail/<slug>/', trade_detail),
    path('orders/', orders_list),
    path('upload/', file_update),
    path('trades/', trades_list),
    path('comment/<uuid>/', trade_comment)
]
