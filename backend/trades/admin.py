from django.contrib import admin
from .models import Trade, Order
from common.utils import human_readble_amount, remove_zeros


from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "N d, Y H:i:s"

@admin.display(description='Price')
def price(obj):
    if obj.price == None:
        return obj.price
    return remove_zeros(obj.price)

@admin.display(description='Stop Price')
def stop_price(obj):
    if obj.stop_price == None:
        return obj.stop_price
    return remove_zeros(obj.stop_price)

@admin.display(description='Limit Price')
def limit_price(obj):
    if obj.limit_price == None:
        return obj.limit_price
    return remove_zeros(obj.limit_price)

@admin.display(description='Start Time')
def start_time(obj):
    if obj.start_time == None:
        return obj.start_time
    return obj.start_time.strftime('%b %d, %Y %H:%M:%S')

@admin.display(description='Last Time')
def last_time(obj):
    if obj.last_time == None:
        return obj.last_time
    return obj.last_time.strftime('%b %d, %Y %H:%M:%S')


@admin.display(description='Op')
def starter_order(obj):
    return obj.starter_order
starter_order.boolean = True

@admin.display(description='Cl')
def closing_order(obj):
    return obj.closing_order
closing_order.boolean = True


#Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('last_time', 'ticker')
    list_display = (
        'ticker',
        'pk',
        'start_time',
        'last_time',
        'in_out',
        starter_order,
        closing_order,
        'trade',
        'action',
        'shares_executed',
        price,
        'status',
        'type',
        'position',
        stop_price,
        limit_price,
        'route',
        'expiration',
        'broker_info',
        'shares',
        'broker',
        'account',
        'broker_ord_id',
        'action_raw',
        'status_raw',
        'type_raw',
        )



@admin.display(description='PNL')
def pnl(obj):
    if obj.pnl == None:
        return obj.pnl
    return remove_zeros(obj.pnl)

@admin.display(description='FEP')
def first_entry_price(obj):
    if obj.first_entry_price == None:
        return obj.first_entry_price
    return remove_zeros(obj.first_entry_price)

@admin.display(description='LEP')
def last_exit_price(obj):
    if obj.last_exit_price == None:
        return obj.last_exit_price
    return remove_zeros(obj.last_exit_price)

@admin.display(description='Cal Com')
def calculated_comissions(obj):
    if obj.calculated_comissions == None:
        return obj.calculated_comissions
    return remove_zeros(obj.calculated_comissions)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    ordering = ('-creation', 'ticker')
    list_display = (
        'ticker',
        'start_time',
        'end_time',
        'duration',
        'max_size',
        'side',
        pnl,
        calculated_comissions,
        'net',
        'entries',
        'exits',
        first_entry_price,
        last_exit_price,
        'closed',
        'position',
        )
    pnl.admin_order_field = 'pnl'
