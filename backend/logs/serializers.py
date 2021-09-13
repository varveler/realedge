from rest_framework import serializers
from .models import TradesTickerLog, TradeTag

class TradesTickerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradesTickerLog
        fields = (  'uuid',
                    'ticker',
                    'date',
                    'user',
                    'comments',
                )


class TagsSerializer(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField()
    class Meta:
        model = TradeTag
        fields = (  'name',
                    'type',
                    'type_display',
                    'selected'
                )

    def get_type_display(self, obj):
        return obj.get_type_display()

    def get_selected(self, obj):
        ticker = self.context.get('ticker')
        date = self.context.get('date')
        print(obj.ticker_date.filter(ticker=ticker, date=date))
        return obj.ticker_date.exists()
        # if self.context.get('selected'):
        #     return self.context.get('selected')
        # return self.context.get('selected')


#ticker_date__ticker=ticker, ticker_date__date=date, ticker_date__
