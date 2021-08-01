from django.urls import path
from .views import homepage, gappers, gapper_detail

urlpatterns = [
    path('', homepage),
    path('data/', gappers ),
    path('gappers/<str:_id>/', gapper_detail, name='gapper_detail'),
]
