from django.contrib import admin
from .models import Trade, Order

# Register your models here.
# @admin.register(Trade)
# class TradeAdmin(admin.ModelAdmin):
#     ordering = ('-date', '-gap_percentage')
#     list_display = (
#         'date',
#         'creation',
#         'ticker',
#         last,
#         'gap_percentage',
#         gap_percentage_display,
#         pm_s2_volume,
#         pm_s1_market_cap,
#         pm_s2_market_cap,
#         pm_s1_float,
#         pm_s2_float,
#         pm_s1_held_percent_insiders,
#         pm_s2_held_percent_insiders,
#         pm_s1_held_percent_institutions,
#         pm_s2_held_percent_institutions,
#         pm_s1_short_percent_float,
#         pm_red_gaps,
#         'pm_observations',
#     )
