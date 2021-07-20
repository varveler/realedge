from django.urls import path
from .views import chart_data

urlpatterns = [
    path('data/<str:uuid>/', chart_data)
]
