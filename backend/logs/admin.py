from django.contrib import admin
from .models import TradesTickerLog, TradeTag, TagTickerDayTrade
# Register your models here.
admin.site.register(TradesTickerLog)
admin.site.register(TradeTag)
admin.site.register(TagTickerDayTrade)
