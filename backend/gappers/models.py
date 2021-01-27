from django.db import models

# Create your models here


class Gapper(models.Model):
    """
        A stock which opens below/above the previous close by a 5% or more
        These tables keeps track of the stock data at the moment of gap
        Also key data after market closes
    """
    class Meta:
        abstract = True

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    market = models.CharField(max_length=20) #NYSE #NASDAQ #pinksheets #ETC
    company_name = models.CharField(max_length=100)

    pm_volume = models.BigIntegerField()
    pm_market_cap = models.BigIntegerField() #market capitalization premarket
    pm_shares_outstanding = models.BigIntegerField()
    pm_float = models.BigIntegerField()
    pm_held_insiders = models.FloatField()
    pm_held_institutions = models.FloatField()
    pm_short_float = models.FloatField(null=True) #percentage
    pm_atr = models.FloatField()
    pm_red_gaps = models.FloatField(null=True) #percentage
    pm_observations = models.IntegerField()

    pdah_volume = models.BigIntegerField() #previous_day_after_hours_volume
    pd_close = models.FloatField() #previous day close

    #After Close Data:
    ac_market_cap = models.BigIntegerField() #after close market capitalization
    volume = models.BigIntegerField()
    gap_percentage = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    tr = models.FloatField()#true range
    move = models.FloatField()
    ac_atr = models.FloatField()#after close ATR
    prev_day_rvol = models.FloatField()
    day_rvol = models.FloatField()
    float_rotation = models.FloatField()


class UpGapper(Gapper):
    pass

class DownGapper(Gapper):
    pass
