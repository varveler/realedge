from django.urls import path
from .views import chart_data, gapper_data

urlpatterns = [
    path('trade/<str:uuid>/', chart_data),
    path('gapper/<str:slug>/', gapper_data)
]
