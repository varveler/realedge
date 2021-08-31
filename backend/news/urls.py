from django.urls import path
from .views import news_list, news_detail, partialnews_list

urlpatterns = [
    path('<ticker>/', news_list),
    path('<uuid>/', news_detail),
    path('partialnews/<ticker>/', partialnews_list)
]
