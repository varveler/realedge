from django.urls import path
from .views import news_list, news_detail

urlpatterns = [
    path('<ticker>/', news_list),
    path('<uuid>/', news_detail),
]
