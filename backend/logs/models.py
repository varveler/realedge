from django.db import models
from reusers.models import ReUser as User
from trades.models import DayTradesGroupedByDayByTicker
import uuid


# Create your models here.
class TradesTickerLog(models.Model):
    class Meta:
        unique_together = ('ticker', 'date', 'user')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()


class TradeTag(models.Model):
    class Meta:
        unique_together = ('name', 'type', 'user')
    ASSERTION = 'AS'
    ERROR = 'ER'
    NEUTRAL = 'NE'
    TYPE_CHOICES = [
        (ASSERTION, 'Assertion'),
        (ERROR, 'Error'),
        (NEUTRAL, 'Neutral')]
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker_date = models.ManyToManyField(DayTradesGroupedByDayByTicker, through='TagTickerDayTrade')

    def __str__(self):
        return "%s BY %s" % (self.name, self.user)

class TagTickerDayTrade(models.Model):
    tradetag = models.ForeignKey(TradeTag, on_delete=models.SET_NULL, related_name='tags', null=True, blank=True)
    grouped_day_trades = models.ForeignKey(DayTradesGroupedByDayByTicker, on_delete=models.SET_NULL, related_name='grouped_trades', null=True, blank=True)


    def __str__(self):
        return '"%s" tag on %s %s by %s' % (self.tradetag.name, self.grouped_day_trades.ticker, self.grouped_day_trades.date, self.tradetag.user)
