from django.urls import path
from .views import homepage, loged_in_gappers, public_gappers, gapper_detail

urlpatterns = [
    path('', homepage),
    path('data/', public_gappers ),
    path('complete-data/', loged_in_gappers ),
    path('gappers/<str:_id>/', gapper_detail, name='gapper_detail'),
]
