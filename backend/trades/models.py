from django.db import models
from reusers.models import ReUser as User
from gappers.models import UpGapper
from django.utils import timezone
from decimal import Decimal
import os
import uuid
import datetime


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

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=200, null=True) #AAPL-open-live-trade-by-varvevler-dasdsassad-sad-asd-asdasdsda-adsads
    closed_slug = models.CharField(max_length=200, null=True) #realedge.io/AAPL-1500-profit-by-varveler-on-may-05-2021-63b40372

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    #str_start_date = models.CharField(max_length=8) #"20210820" YYYYMMDD
    #str_end_date = models.CharField(max_length=8) #"20210820" YYYYMMDD

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

    comments = models.TextField(default='', null=True)

    @property
    def str_start_date(self):
        return datetime.datetime.strftime(self.start_time, '%Y%m%d')

    @property
    def str_end_date(self):
        return datetime.datetime.strftime(self.end_time, '%Y%m%d')

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

    def set_trade_final_slug(self):
        if self.closed:
            small_uuid = str(self.uuid).split('-')[0]
            p_or_l = 'profit' if self.pnl >= 0 else 'loss'
            close_date = datetime.datetime.strftime(self.end_time, '%b-%d-%Y').lower()
            self.closed_slug = '{ticker}-{pnl}-{p_or_l}-by-{username}-on-{close_date}-{small_uuid}'.format(
                                                    ticker = self.ticker,
                                                    pnl = abs(int(self.pnl)),
                                                    p_or_l = p_or_l,
                                                    username = self.user.user_name,
                                                    close_date = close_date,
                                                    small_uuid = small_uuid)
            self.save()


    def set_self_slug(self):
        if not self.slug:
            small_uuid = '-'.join(str(self.uuid).split('-')[0:2])
            self.slug = '{ticker}-open-live-trade-by-{username}-{uuid}'.format(
                                                        ticker = self.ticker,
                                                        username = self.user.user_name,
                                                        uuid = small_uuid)
            self.save()




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
                    new_trade.set_self_slug()
                    self.trade = new_trade
                    self.starter_order = True
                    self.in_out = self.InOut.IN
                    self.position = pos
                else: # there is parent trade so there must be an open trade
                    parent_trade = parent_trades.get() # update a Trade relate order
                    if parent_trade.side == Trade.SHORT: # parent is a short
                        if self.action in [Order.SHORT, Order.SELL]: #adding
                            self.in_out = self.InOut.IN # adding
                            pos = parent_trade.position + int(self.shares_executed) * (-1)  #ex. -100 + 100 *-1 = -200
                            self.position = pos
                            parent_trade.position = pos
                            parent_trade.entries = parent_trade.entries + 1
                            parent_trade.pnl_accumulator += self.price * self.shares_executed
                            parent_trade.max_size = pos * (-1)
                        else: # buying to cover
                            self.in_out = self.InOut.OUT
                            pos = parent_trade.position + int(self.shares_executed)  #ex.  -300 + 100 = -200
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
                    parent_trade.set_trade_final_slug()
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


class TradesGroupedByDayByTicker(Trade):
    class Meta:
        abstract = True

    def __init__(self, trades):
        self.trades = trades
        self.trades_count = 0

    def group_trades(self, trades):
        days = []
        format = '%Y-%m-%d'
        for trade in trades:
            if trade.start_time.date().strftime(format) not in days:
                days.append(trade.start_time.date().strftime(format))
        # group them together with a dict  like {'2021-04-30': {}, '2021-05-12': {}, '2021-05-13': {}}
        grouped_trades_by_day = {k: {} for k in days}
        for day in days:
            trades_day = trades.filter(start_time__year=day[0:4], start_time__month=day[5:7], start_time__day=day[8:10])
            grouped_trades_by_day[day] = trades_day
        for date, trades in grouped_trades_by_day.items():
            tickers = [] # get a list of tickers ['MOTH', 'AAPL', 'GME']
            [tickers.append(trade.ticker) for trade in trades if trade.ticker not in tickers]
            grouped_trades_by_ticker = {k: trades.filter(ticker=k) for k in tickers}
            # inser them in dict like {'2021-04-30': {'MOTH': queryset[trades...]}, '2021-05-12': {'AAPL': queryset[trades...]}, '2021-05-13': {'GME': queryset[trades...]}}
            grouped_trades_by_day[date] = grouped_trades_by_ticker
        # itereate over each day, each ticker to aggregata data and give final dictionary
        for date, ticker in grouped_trades_by_day.items():
            for ticker, trades in ticker.items():
                pnl = remove_zeros(trades.aggregate(Sum('pnl'))['pnl__sum'])
                shares_traded = str(trades.aggregate(Sum('max_size'))['max_size__sum'])
                #calculate if short, long or both
                sides = list(set([trade.side for trade in trades])) #['SH', 'SH','SH', 'LO'] to ['SH', 'LO']
                first = 'short' if sides[0] == 'SH' else 'long'
                side = 'both' if len(sides) > 1 else first
                calculated_comissions = remove_zeros(trades.aggregate(Sum('calculated_comissions'))['calculated_comissions__sum'])
                net = str(trades.aggregate(Sum('net'))['net__sum'])
                serializer = DisplayTradeSerializer(trades, many=True)
                grouped_trades_by_day[date][ticker] = {'trades_count': trades.count(),
                                                        'pnl': pnl,
                                                        'side': side,
                                                        'calculated_comissions': calculated_comissions,
                                                        'net': net,
                                                        'shares_traded': shares_traded,
                                                        'trades': serializer.data,
                                                        }
        return grouped_trades_by_day
