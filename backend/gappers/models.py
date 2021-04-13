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
    market = models.CharField(max_length=20) # NYSE #NASDAQ #pinksheets #ETC
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    # PreMarket Data Source 1
    pm_source1 = models.CharField(max_length=30) # Yahoo
    pm_s1_volume = models.BigIntegerField(null=True)
    pm_s1_market_cap = models.BigIntegerField(null=True) # market capitalization premarket
    pm_s1_shares_outstanding = models.BigIntegerField(null=True)
    pm_s1_float = models.BigIntegerField(null=True)
    pm_s1_held_insiders = models.FloatField(null=True)
    pm_s1_held_institutions = models.FloatField(null=True)
    pm_s1_short_float = models.FloatField(null=True) # percentage
    pm_s1_beta = models.FloatField(null=True) # percentage
    #  PreMarket Data Source 2
    pm_source2 = models.CharField(max_length=30) # Barchar
    pm_s2_volume = models.BigIntegerField(null=True)
    pm_s2_market_cap = models.BigIntegerField(null=True) # market capitalization premarket
    pm_s2_shares_outstanding = models.BigIntegerField(null=True)
    pm_s2_float = models.BigIntegerField(null=True)
    pm_s2_held_insiders = models.FloatField(null=True)
    pm_s2_held_institutions = models.FloatField(null=True)
    pm_s2_short_float = models.FloatField(null=True)
    # Calculated Data PreMarket
    pm_atr = models.FloatField(null=True)
    pm_red_gaps = models.FloatField(null=True) # percentage
    pm_observations = models.IntegerField(null=True)

    # Prev Day Data
    pdah_volume = models.BigIntegerField(null=True) # previous_day_after_hours_volume
    pd_close = models.FloatField(null=True) # previous day close
    pd_rvol = models.FloatField(null=True)

    # At Close Data: 4PM
    ac_float = models.BigIntegerField(null=True)
    ac_market_cap = models.BigIntegerField(null=True) # after close market capitalization
    volume = models.BigIntegerField(null=True)
    gap_percentage = models.FloatField(null=True)
    gap = models.FloatField(null=True)
    open = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    close = models.FloatField(null=True)
    last = models.FloatField(null=True)
    tr = models.FloatField(null=True)  # true range
    move = models.FloatField(null=True)
    ac_atr = models.FloatField(null=True)  # after close ATR
    day_rvol = models.FloatField(null=True)
    float_rotation = models.FloatField(null=True)


class UpGapper(Gapper):
    pass


class DownGapper(Gapper):
    pass
