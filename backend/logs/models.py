from django.db import models

from gappers.models import UpGapper
# Create your models here.


class Trade(models.Model):
    SHORT = 'SH'
    LONG = 'LO'
    SIDE_CHOICES = [
        (SHORT, 'Short'),
        (LONG, 'Long')]

    DAYTRADE = 'DT'
    SCALP = 'SC'
    SWING = 'SW'
    TYPE_CHOICES = [
        (DAYTRADE, 'Day Trade'),
        (SCALP, 'Scalp'),
        (SWING, 'Swing')]

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    ticker = models.CharField(max_length=10)
    market = models.CharField(max_length=20) # NYSE #NASDAQ #pinksheets #ETC
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    side = models.CharField(max_length=2, choices=SIDE_CHOICES)#short or long
    type = models.CharField(max_length=2, choices=TYPE_CHOICES) #daytrade, scalp, swing
    pnl = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=10)
    net = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=10)
    duration = models.IntegerField()
    size = models.PositiveIntegerField() #100 200 300 400 500 1000 20,000
    entries = models.PositiveIntegerField()
    exits = models.PositiveIntegerField()
    entry_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    exit_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)

    comissions = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    borrow_comissions = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    upgapper = models.ForeignKey(UpGapper, on_delete=models.PROTECT, null=True, blank=True)
    closed = models.BooleanField(default=True)
    #assertions
    #errors

class Order(models.Model):
    SHORT = 'SH'
    BUY = 'BU'
    SELL = 'SE'
    ACTION_CHOICES = [
        (SHORT, 'Short'),
        (BUY, 'Buy'),
        (SELL, 'Sell')]

    MARKET = 'MA'
    LIMIT = 'LI'
    STOP_LIMIT = 'SL'
    STOP_MARKET = 'SM'
    TYPE_CHOICES = [
        (MARKET, 'Market'),
        (LIMIT, 'Limit'),
        (STOP_LIMIT, 'Stop Limit'),
        (STOP_MARKET, 'Stop Market')]

    FILLED = 'FI'
    CANCELED = 'CA'
    REJECTED = 'RE'
    STATUS_CHOICES = [
        (FILLED, 'Filled'),
        (CANCELED, 'Canceled'),
        (REJECTED, 'Rejected')]

    class InOut(models.IntegerChoices):
        IN = 1
        OUT = 2

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    last_time = models.DateTimeField(null=True, blank=True)

    ticker = models.CharField(max_length=10)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES) #Short, Buy, Sell
    shares = models.IntegerField()

    status = models.CharField(max_length=2, choices=STATUS_CHOICES) # Filled, Canceled, Rejected
    type = models.CharField(max_length=2, choices=TYPE_CHOICES) # market, limit, stop market, stop limit
    price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    stop_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    limit_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    in_out = models.IntegerField(choices=InOut.choices)
    position = models.IntegerField(null=True, blank=True) # cumulative position-100, #-200, #0
    expiration = models.CharField(max_length=50)

    broker = models.CharField(max_length=30)
    broker_ord_id = models.CharField(max_length=50)
    broker_info = models.CharField(max_length=50)

    trade = models.ForeignKey(Trade, on_delete=models.PROTECT, null=True, blank=True)
