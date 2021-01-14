from django.urls import path
from .views import fundamentals

urlpatterns = [
    path('fundamentals/', fundamentals),
]
