from django.db import models
from django.contrib.auth.models import User
from gappers.models import UpGapper
import os
from django.utils import timezone
from decimal import Decimal

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

    OPEN = 'OP'
    CLOSED = 'CL'
    PARTIALLY_CLOSED = 'PC'

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    ticker = models.CharField(max_length=10)
    market = models.CharField(max_length=20) # NYSE #NASDAQ #pinksheets #ETC
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    side = models.CharField(max_length=2, choices=SIDE_CHOICES)#short or long
    type = models.CharField(max_length=2, choices=TYPE_CHOICES) #daytrade, scalp, swing
    pnl = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=10)
    net = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=10)

    comissions = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=10)
    calculated_comissions = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=10)
    borrow_comissions = models.DecimalField(null=True, max_digits=22, decimal_places=10)
    ecn_fees = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=10)

    #dependent of orders fields:
    closed = models.BooleanField(default=False)
    position = models.IntegerField(null=True) #-100 -200 0 100 200 300 400 500 1000 20,000
    max_size = models.PositiveIntegerField(null=True) #100 200 300 400 500 1000 20,000
    entries = models.PositiveIntegerField(null=True)
    exits = models.PositiveIntegerField(null=True)
    first_entry_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    last_exit_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    duration = models.DurationField(null=True)
    pnl_accumulator = models.DecimalField(null=True, blank=True, max_digits=31, decimal_places=10)

    upgapper = models.ForeignKey(UpGapper, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def calculate_comissions(self):
        filled_orders = self.order_set.filter(status=Order.FILLED)
        acumulator = 0
        for order in filled_orders:
            if order.shares_executed < 200:
                acumulator += Decimal(0.99)
            else:
                if order.type in [Order.MARKET or Order.STOP_MARKET] or order.start_time == order.last_time:#inmidiatly filled (not free)
                    acumulator += order.shares_executed * Decimal(0.005)
        return acumulator





class Order(models.Model):
    class Meta:
        unique_together = ('user', 'broker_ord_id', 'start_time')
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
    action_raw = models.CharField(max_length=15)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES) #Short, Buy, Sell
    shares = models.PositiveIntegerField() #the shares inputed by the user in tehir platform
    shares_executed = models.PositiveIntegerField(null=True) #the # of filled shares
    shares_display = models.PositiveIntegerField(null=True)
    status_raw = models.CharField(max_length=15)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES) # Filled, Canceled, Rejected
    type_raw = models.CharField(max_length=15)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES) # market, limit, stop market, stop limit
    price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10) #execution price
    stop_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    limit_price = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    route = models.CharField(max_length=20)
    expiration = models.CharField(max_length=50)

    broker = models.CharField(max_length=30)
    account = models.CharField(max_length=25)
    broker_ord_id = models.CharField(max_length=100)
    broker_info = models.CharField(max_length=300)

    calculated_commission = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    commission = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)
    ecn_fees = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=10)

    # related to other orders
    in_out = models.IntegerField(choices=InOut.choices, null=True)
    starter_order = models.BooleanField(default=False) # is this an order that starts a trade?
    closing_order = models.BooleanField(default=False) # is this an order that closes a trade?
    position = models.IntegerField(null=True, blank=True) # cumulative position-100, #-200, #0

    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)




    def save(self, *args, **kwargs):
        """
        Save override to create Trades and fill fields related to other orders that allow to keep process order and fill Trades
        """
        if self.pk is None:
            if self.status is self.FILLED: #first time creating this Order that affects in_out, posstion, starter_order, closing_order,
                parent_trades = Trade.objects.filter(user=self.user, ticker=self.ticker, closed=False) #broker #account
                if parent_trades.count() > 1:
                    raise ValueError("Invalid data there is more than 1 open trade with this ticker")
                if not parent_trades: # create parent trade, first entry order
                    pos = int(self.shares_executed) * (-1) if self.action in [Order.SHORT, Order.SELL] else int(self.shares_executed)
                    new_trade = Trade.objects.create(
                        user = self.user,
                        start_time = self.last_time,
                        ticker = self.ticker,
                        side = Trade.SHORT if self.action in [Order.SHORT, Order.SELL] else Trade.LONG,
                        first_entry_price = self.price,
                        position = pos,
                        entries = 1,
                        pnl_accumulator = self.price * self.shares_executed,
                        max_size = self.shares_executed)
                    self.trade = new_trade
                    self.starter_order = True
                    self.in_out = self.InOut.IN
                    self.position = pos
                else: # open trade
                    parent_trade = parent_trades.get() # update a Trade relate order
                    if parent_trade.side == Trade.SHORT: # parent is a short
                        if self.action in [Order.SHORT, Order.SELL]: #adding
                            self.in_out = self.InOut.IN # adding
                            pos = parent_trade.position + int(self.shares_executed) * (-1)  # -100 + 100 *-1 = -200
                            self.position = pos
                            parent_trade.position = pos
                            parent_trade.entries = parent_trade.entries + 1
                            parent_trade.pnl_accumulator += self.price * self.shares_executed
                            parent_trade.max_size = pos * (-1)
                        else: # buying to cover
                            self.in_out = self.InOut.OUT
                            pos = parent_trade.position + int(self.shares_executed)  # -300 + 100 = -200
                            self.position = pos
                            parent_trade.position = pos
                            parent_trade.exits = (parent_trade.exits if parent_trade.exits else 0) + 1
                            parent_trade.pnl_accumulator -= self.price * self.shares_executed
                            if pos == 0: # means the last order and we were closing the Trade in this order
                                self.closing_order = True
                                parent_trade.closed = True
                                parent_trade.end_time = self.last_time
                                parent_trade.last_exit_price = self.price
                                parent_trade.pnl = parent_trade.pnl_accumulator
                                parent_trade.duration = self.last_time - timezone.localtime(parent_trade.start_time)
                                parent_trade.calculated_comissions = parent_trade.calculate_comissions
                    else: # parent is a long
                        if self.action in [Order.SHORT, Order.SELL]: # sell to cover
                            self.in_out = self.InOut.OUT
                            pos = parent_trade.position - int(self.shares_executed)
                            self.position = pos
                            parent_trade.position = pos
                            parent_trade.exits = (parent_trade.exits if parent_trade.exits else 0) + 1
                            parent_trade.pnl_accumulator -= self.price * self.shares_executed
                            if pos == 0: # means this is the last order of the Trade
                                self.closing_order = True
                                parent_trade.closed = True
                                parent_trade.end_time = self.last_time
                                parent_trade.last_exit_price = self.price
                                parent_trade.pnl = parent_trade.pnl_accumulator * (-1)
                                parent_trade.duration = self.last_time - timezone.localtime(parent_trade.start_time)
                                parent_trade.calculated_comissions = parent_trade.calculate_comissions
                        else: # adding
                            self.in_out = self.InOut.IN
                            pos = parent_trade.position + int(self.shares_executed)
                            self.position = pos
                            parent_trade.position = pos
                            parent_trade.entries = parent_trade.entries + 1
                            parent_trade.pnl_accumulator += self.price * self.shares_executed
                            parent_trade.max_size = pos
                    self.trade = parent_trade
                    parent_trade.save()
        super(Order, self).save(*args, **kwargs)







class OrdersFile(models.Model):
    _file = models.FileField(upload_to='tempOrdersFiles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self,*args,**kwargs):
        if os.path.isfile(self._file.path):
            os.remove(self._file.path)
        super(OrdersFile, self).delete(*args,**kwargs)

    def __str__(self):
        return os.path.basename(self._file.name)
