from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma

# Register your models here.
from .models import UpGapper
from common.utils import human_readble_amount, remove_zeros

@admin.display(description='Gap %')
def gap_percentage_display(obj):
    if obj.gap_percentage == None:
        return obj.gap_percentage
    return (str(obj.gap_percentage * 100))[:5] + '%'

@admin.display(description='Volume')
def pm_s2_volume(obj):
    return intcomma(obj.pm_s2_volume)

@admin.display(description='Mkt Cap s1')
def pm_s1_market_cap(obj):
    if obj.pm_s1_market_cap == None:
        return obj.pm_s1_market_cap
    return human_readble_amount(obj.pm_s1_market_cap)


@admin.display(description='Mkt Cap s2')
def pm_s2_market_cap(obj):
    if obj.pm_s2_market_cap == None:
        return obj.pm_s2_market_cap
    return human_readble_amount(obj.pm_s2_market_cap)


@admin.display(description='Float s1')
def pm_s1_float(obj):
    if obj.pm_s1_float == None:
        return obj.pm_s1_float
    return human_readble_amount(obj.pm_s1_float)


@admin.display(description='Float s2')
def pm_s2_float(obj):
    if obj.pm_s2_float == None:
        return obj.pm_s2_float
    return human_readble_amount(obj.pm_s2_float)

@admin.display(description='Held Insid s1')
def pm_s1_held_percent_insiders(obj):
    if obj.pm_s1_held_percent_insiders == None:
        return obj.pm_s1_held_percent_insiders
    return (str(obj.pm_s1_held_percent_insiders * 100))[:5] + '%'

@admin.display(description='Held Insid s2')
def pm_s2_held_percent_insiders(obj):
    if obj.pm_s2_held_percent_insiders == None:
        return obj.pm_s2_held_percent_insiders
    return str(remove_zeros(obj.pm_s2_held_percent_insiders)) + '%'

@admin.display(description='Held Inst s1')
def pm_s1_held_percent_institutions(obj):
    if obj.pm_s1_held_percent_institutions == None:
        return obj.pm_s1_held_percent_institutions
    return (str(obj.pm_s1_held_percent_institutions * 100))[:5] + '%'

@admin.display(description='Held Inst s2')
def pm_s2_held_percent_institutions(obj):
    if obj.pm_s2_held_percent_institutions == None:
        return obj.pm_s2_held_percent_institutions
    return str(remove_zeros(obj.pm_s2_held_percent_institutions)) + '%'

@admin.display(description='Short % of Float')
def pm_s1_short_percent_float(obj):
    if obj.pm_s1_short_percent_float == None:
        return obj.pm_s1_short_percent_float
    return (str(obj.pm_s1_short_percent_float * 100))[:5] + '%'


@admin.display(description='Price')
def last(obj):
    if obj.last == None:
        return obj.last
    return remove_zeros(obj.last)

@admin.display(description='Red Gap Prob%')
def pm_red_gaps(obj):
    if obj.pm_red_gaps == None:
        return obj.pm_red_gaps
    return str(remove_zeros(obj.pm_red_gaps))+'%'

@admin.register(UpGapper)
class UpGapperAdmin(admin.ModelAdmin):
    ordering = ('date', '-gap_percentage')
    list_display = (
        'date',
        'ticker',
        last,
        'gap_percentage',
        gap_percentage_display,
        pm_s2_volume,
        pm_s1_market_cap,
        pm_s2_market_cap,
        pm_s1_float,
        pm_s2_float,
        pm_s1_held_percent_insiders,
        pm_s2_held_percent_insiders,
        pm_s1_held_percent_institutions,
        pm_s2_held_percent_institutions,
        pm_s1_short_percent_float,
        pm_red_gaps,
        'pm_observations',
    )
