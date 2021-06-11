from django.urls import path
from .views import homepage, gappers

urlpatterns = [
    path('', homepage),
    path('data/', gappers )
]
