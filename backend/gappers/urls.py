from django.urls import path
from .views import homepage, gappers, gapper_detail_view

urlpatterns = [
    path('', homepage),
    path('data/', gappers ),
    path('gappers/<str:_id>/', gapper_detail_view, name='gapper_detail_view'),
]
