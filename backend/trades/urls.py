from django.urls import path
from .views import (trade_detail,
                    orders_list,
                    file_update,
                    trades_list,
                    trade_comment,
                    grouped_trades_by_day_by_ticker,
                    grouped_trade_detail
                    )

urlpatterns = [
    path('detail/<slug>/', trade_detail),
    path('groupeddetails/<slug>/', grouped_trade_detail),
    path('orders/', orders_list),
    path('upload/', file_update),
    path('trades/', trades_list),
    path('comment/<uuid>/', trade_comment),
    path('byticker/', grouped_trades_by_day_by_ticker),
    #path('detailByTicker/', trade_detail_by_day_by_ticker),
]
