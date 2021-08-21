from django.urls import path
from .views import chart_data, gapper_data

urlpatterns = [
    path('trade/', chart_data),
    path('gapper/<str:slug>/', gapper_data)
]
