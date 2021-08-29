from rest_framework import serializers
from .models import Order, Trade
from reusers.models import ReUser
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .admin import pnl, first_entry_price, calculated_comissions, last_exit_price
from django.contrib.humanize.templatetags.humanize import naturaltime
from common.utils import remove_zeros
import datetime


class TZChoiceField(serializers.ChoiceField):

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''
        if data == 'MKT':
            return 'MA'
        elif data == 'LMT':
            return 'LI'
        elif data == 'Stop_MKT':
            return 'SM'
        elif data == 'Stop_LMT':
            return 'SL'
        for key, val in self._choices.items():
            if val == data:
                return key
            elif val == data.capitalize():
                return key
        self.fail('invalid_choice', input=data)


class BlankableDecimalField(serializers.DecimalField):
    """
    We wanted to be able to receive an empty string ('') for a decimal field
    and in that case turn it into a None number
    """
    def to_internal_value(self, data):
        if data == '':
            return None

        return super(BlankableDecimalField, self).to_internal_value(data)

class ReUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReUser
        fields = ('username', )


class TZOrderSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%H:%M:%S %Y/%m/%d')
    last_time = serializers.DateTimeField(format='%H:%M:%S %Y/%m/%d')
    action = TZChoiceField(Order.ACTION_CHOICES)
    status = TZChoiceField(Order.STATUS_CHOICES)
    type = TZChoiceField(Order.TYPE_CHOICES)
    price = BlankableDecimalField(max_digits=16, decimal_places=10)
    stop_price = BlankableDecimalField(max_digits=16, decimal_places=10)
    limit_price = BlankableDecimalField(max_digits=16, decimal_places=10)
    broker = serializers.CharField(required=False, allow_blank=True)
    broker_info = serializers.CharField(required=False, allow_blank=True)
    #user = serializers.HiddenField( default=serializers.CurrentUserDefault())
    user = serializers.PrimaryKeyRelatedField(queryset=ReUser.objects.all())

    class Meta:
        model = Order
        fields = [
            'start_time',
            'last_time',
            'ticker',
            'action',
            'action_raw',
            'shares',
            'shares_executed',
            'status',
            'status_raw',
            'type',
            'route',
            'type_raw',
            'price',
            'stop_price',
            'limit_price',
            'expiration',
            'broker',
            'account',
            'broker_ord_id',
            'broker_info',
            'user',
        ]

    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            # If we are instantiating with data={something}
            try:
                # Try to get the object in question
                obj = Order.objects.get(user=self.initial_data['user'], start_time=self.initial_data['start_time'], broker_ord_id=self.initial_data['broker_ord_id'])
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                # Except not finding the object or the data being ambiguous
                # for defining it. Then validate the data as usual
                return super().is_valid(raise_exception)
            else:
                # If the object is found add it to the serializer. Then
                # validate the data as usual
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            # If the Serializer was instantiated with just an object, and no
            # data={something} proceed as usual
            return super().is_valid(raise_exception)



class OrderSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%H:%M:%S %Y/%m/%d')
    last_time = serializers.DateTimeField(format='%H:%M:%S %Y/%m/%d')
    action = TZChoiceField(Order.ACTION_CHOICES)
    status = TZChoiceField(Order.STATUS_CHOICES)
    type = TZChoiceField(Order.TYPE_CHOICES)
    price = BlankableDecimalField(max_digits=16, decimal_places=10)
    stop_price = BlankableDecimalField(max_digits=16, decimal_places=10)
    limit_price = BlankableDecimalField(max_digits=16, decimal_places=10)
    broker = serializers.CharField(required=False, allow_blank=True)
    broker_info = serializers.CharField(required=False, allow_blank=True)
    user = serializers.PrimaryKeyRelatedField(queryset=ReUser.objects.all())
    no_zeros_price = serializers.SerializerMethodField()
    no_zeros_stop_price = serializers.SerializerMethodField()
    no_zeros_limit_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'start_time',
            'last_time',
            'ticker',
            'action',
            'action_raw',
            'shares',
            'shares_executed',
            'status',
            'status_raw',
            'type',
            'route',
            'type_raw',
            'price',
            'stop_price',
            'limit_price',
            'expiration',
            'broker',
            'account',
            'broker_ord_id',
            'broker_info',
            'user',
            'no_zeros_price',
            'no_zeros_stop_price',
            'no_zeros_limit_price',
        ]
    def get_no_zeros_price(self, obj):
        if obj.price == None:
            return obj.price
        return remove_zeros(obj.price)

    def get_no_zeros_stop_price(self, obj):
        if obj.stop_price == None:
            return obj.stop_price
        return remove_zeros(obj.stop_price)

    def get_no_zeros_limit_price(self, obj):
        if obj.limit_price == None:
            return obj.limit_price
        return remove_zeros(obj.limit_price)


    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            # If we are instantiating with data={something}
            try:
                # Try to get the object in question
                obj = Order.objects.get(user=self.initial_data['user'], start_time=self.initial_data['start_time'], broker_ord_id=self.initial_data['broker_ord_id'])
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                # Except not finding the object or the data being ambiguous
                # for defining it. Then validate the data as usual
                return super().is_valid(raise_exception)
            else:
                # If the object is found add it to the serializer. Then
                # validate the data as usual
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            # If the Serializer was instantiated with just an object, and no
            # data={something} proceed as usual
            return super().is_valid(raise_exception)


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'creation',
            'update',
            'date',
            'start_time',
            'end_time',
            'ticker',
            'market',
            'company_name',
            'industry',
            'side',
            'type',
            'pnl',
            'net',
            'duration',
            'size',
            'entries',
            'exits',
            'entry_price',
            'exit_price',
            'comissions',
            'borrow_comissions',
            'upgapper',
            'closed',
            ]

class DisplayTradeSerializer(serializers.ModelSerializer):
    pnl = serializers.SerializerMethodField()
    calculated_comissions = serializers.SerializerMethodField()
    first_entry_price = serializers.SerializerMethodField()
    last_exit_price = serializers.SerializerMethodField()
    orders = TZOrderSerializer(source='order_set', many=True)
    natural_time = serializers.SerializerMethodField()
    str_start_date = serializers.SerializerMethodField()
    class Meta:
        model = Trade
        fields = ['ticker',
                  'start_time',
                  'end_time',
                  'duration',
                  'max_size',
                  'side',
                  'pnl',
                  'calculated_comissions',
                  'net',
                  'entries',
                  'exits',
                  'first_entry_price',
                  'last_exit_price',
                  'closed',
                  'position',
                  'slug',
                  'closed_slug',
                  'uuid',
                  'orders',
                  'natural_time',
                  'comments',
                  'uuid',
                  'str_start_date']

    def get_pnl(self, obj):
        return pnl(obj)

    def get_calculated_comissions(self, obj):
        return calculated_comissions(obj)

    def get_first_entry_price(self, obj):
        return first_entry_price(obj)

    def get_last_exit_price(self, obj):
        return last_exit_price(obj)

    def get_natural_time(self, obj):
        return naturaltime(obj.start_time)

    def get_str_start_date(self, obj):
        return datetime.datetime.strftime(obj.start_time, '%Y%m%d')

#class TradesGroupedByDayByTickerSerializer(serializers.Serializer):



"""
[
{
"start_time": "09:41:12 2021/04/26",
"last_time": "09:41:12 2021/04/26",
"ticker": "OCGN",
"action": "SELL",
"shares": "100",
"status": "Filled",
"type": "MKT",
"price": "11.22",
"stop_price": "",
"limit_price": "",
"in_out": "",
"position": "",
"expiration": "DAY",
"broker": "",
"broker_ord_id": "dEVA81525.0426084114.2",
"broker_info": ""},
{
"start_time": "09:40:46 2021/04/26",
"last_time": "09:40:46 2021/04/26",
"ticker": "OCGN",
"action": "BUY",
"shares": "100",
"status": "Filled",
"type": "MKT",
"price": "11.3",
"stop_price": "",
"limit_price": "",
"in_out": "",
"position": "",
"expiration": "DAY",
"broker": "",
"broker_ord_id": "dEVA81525.0426084049.1",
"broker_info": ""
}
]
"""
