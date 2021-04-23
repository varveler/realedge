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
        ordering = ['-date', '-gap_percentage'] #Sort in asc order
        unique_together = ['date', 'ticker']

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
    pm_s1_held_percent_insiders = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_s1_held_percent_institutions = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_s1_short_percent_float = models.DecimalField(null=True, max_digits=16, decimal_places=10) # percentage
    pm_s1_shares_short = models.BigIntegerField(null=True)
    pm_s1_beta = models.DecimalField(null=True, max_digits=16, decimal_places=10) # percentage

    #  PreMarket Data Source 2
    pm_source2 = models.CharField(max_length=30) # Barchar
    pm_s2_volume = models.BigIntegerField(null=True)
    pm_s2_market_cap = models.BigIntegerField(null=True) # market capitalization premarket
    pm_s2_shares_outstanding = models.BigIntegerField(null=True)
    pm_s2_float = models.BigIntegerField(null=True)
    pm_s2_held_percent_insiders = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_s2_held_percent_institutions = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_s2_short_percent_float = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_s2_shares_short = models.BigIntegerField(null=True)
    # Calculated Data PreMarket
    pm_atr = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    pm_red_gaps = models.DecimalField(null=True, max_digits=16, decimal_places=10) # percentage
    pm_observations = models.IntegerField(null=True)

    # Prev Day Data
    pdah_volume = models.BigIntegerField(null=True) # previous_day_after_hours_volume
    pd_close = models.DecimalField(null=True, max_digits=16, decimal_places=10) # previous day close
    pd_rvol = models.DecimalField(null=True, max_digits=16, decimal_places=10)

    # At Close Data: 4PM
    ac_float = models.BigIntegerField(null=True)
    ac_market_cap = models.BigIntegerField(null=True) # after close market capitalization
    volume = models.BigIntegerField(null=True)
    gap_percentage = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    gap = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    open = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    high = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    low = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    close = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    last = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    tr = models.DecimalField(null=True, max_digits=16, decimal_places=10)  # true range
    move = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    ac_atr = models.DecimalField(null=True, max_digits=16, decimal_places=10) # after close ATR
    day_rvol = models.DecimalField(null=True, max_digits=16, decimal_places=10)
    float_rotation = models.DecimalField(null=True, max_digits=16, decimal_places=10)


    def __str__(self):
        return '{date} {ticker} {gap_percentage} {pm_s2_volume}'.format(
                                        date = self.date,
                                        ticker = self.ticker,
                                        gap_percentage = self.gap_percentage,
                                        pm_s2_volume = self.pm_s2_volume)


class UpGapper(Gapper):
    pass


class DownGapper(Gapper):
    pass
