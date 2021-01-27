from django.db import models

# Create your models here.
class Trade(models.Model):

    class Type(models.TextChoices):
        LONG = 'L', _('Long')
        SHORT = 'S', _('Short')
    type = models.CharField(max_length=1, choices=Type.choices)

    first_entry_date = models.DateTimeField()
    last_exit_date = models.DateTimeField()
    gross_profit = models.FloatField() # 120.23
    net_profit = models.FloatField() # minus commissions and fees 115.5
    duration = models.DurationField()
    duration_seconds = models.IntegerField() # 142
    max_size = models.IntegerField() # 400
    entries = models.IntegerField() # 1
    exits = models.IntegerField() # 2
    comments = models.TextField()



class Order(models.Model):
    class InOrOut(models.TextChoices):
        IN = 'I', _('In')
        OUT = 'O', _('Out')
    in_or_out = models.CharField(max_length=1, choices=InOrOut.choices, default='')

    class Side(models.TextChoices):
        BUY_LONG = 'BL', _('Buy Long')
        BUY_COVER = 'BC', _('Buy Cover')
        SELL = 'SC', _('Sell Cover')
        SHORT = 'SH', _('Short')
    side = models.CharField(max_length=2, choices=Side.choices)

    class Type(models.TextChoices):
        MARKET = 'MA', _('Market')
        LIMIT = 'LI', _('Limit')
        STOP_MARKET = 'SL', _('Stop Limit')
        STOP_LIMIT = 'SM', _('Stop Market')
        PROFIT_MARKET = 'PM', _('Profit Market')
        PROFIT_LIMIT = 'PL', _('Profit Limit')
    type = models.CharField(max_length=2, choices=Type.choices)

    class Status(models.TextChoices):
        FILLED = 'F', _('Filled')
        CANCELED = 'C', _('Canceled')
    status = models.CharField(max_length=2, choices=Status.choices)

    creation = models.DateTimeField(auto_now_add=True) #at the database

    placed_time = models.DateTimeField()
    execution_time = models.DateTimeField()

    price = models.FloatField(null=True)
    execution_price = models.FloatField(null=True)

    shares = models.PositiveIntegerField()
    position = models.IntegerField() #after the trade

    commission = models.FloatField(null=True)
    ecn_fees = models.FloatField(null=True)
    locate_fees = models.FloatField(null=True)
    #broker = models.CharField(max_length=)

    trade = models.ForeignKey(Trade, on_delete=models.PROTECT)





    #orders = models.IntegerField()
    #setup_name =
    #broker =
