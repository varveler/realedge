from rest_framework import serializers
from .models import TradesTickerLog

class TradesTickerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradesTickerLog
        fields = (  'uuid',
                    'ticker',
                    'date',
                    'user',
                    'comments',
                )
