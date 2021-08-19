from django.urls import path
from .views import (trade_detail,
                    orders_list,
                    file_update,
                    trades_list,
                    trade_comment,
                    grouped_trades_by_day_by_ticker,
                    )

urlpatterns = [
    path('detail/<slug>/', trade_detail),
    path('orders/', orders_list),
    path('upload/', file_update),
    path('trades/', trades_list),
    path('comment/<uuid>/', trade_comment),
    path('byticker/', grouped_trades_by_day_by_ticker),
    #path('byticker2/', grouped_trades_by_day_by_ticker2),
]
