from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import Trade, Order

@receiver(post_save, sender=Trade)
def update_non_filled_orders_and_calculate_comissions(sender, instance, created, **kwargs):
    """
    When a trade is saved this func is called on post save signal
    if the order is closed executes marks missing orders with the
    corresponding Trade and caluclates commission
    """
    if instance.closed:
        orders = Order.objects.filter(ticker=instance.ticker).filter(Q( last_time__gte=instance.start_time, start_time__lte=instance.end_time) | Q(start_time__lte=instance.end_time, last_time__gte=instance.start_time)).exclude(status=Order.FILLED)
        for order in orders:
            order.trade = instance
            order.save()
