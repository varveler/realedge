from .models import UpGapper
from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from .admin import (gap_percentage_display,
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
                    last,
                    pm_red_gaps)


class GapperSerializer(serializers.ModelSerializer):
    last = serializers.SerializerMethodField()
    gap_percentage_display = serializers.SerializerMethodField()
    pm_s2_volume = serializers.SerializerMethodField()
    pm_s1_market_cap = serializers.SerializerMethodField()
    pm_s2_market_cap = serializers.SerializerMethodField()
    pm_s1_float = serializers.SerializerMethodField()
    pm_s2_float = serializers.SerializerMethodField()
    pm_s1_held_percent_insiders = serializers.SerializerMethodField()
    pm_s2_held_percent_insiders = serializers.SerializerMethodField()
    pm_s1_held_percent_institutions = serializers.SerializerMethodField()
    pm_s2_held_percent_institutions = serializers.SerializerMethodField()
    pm_s1_short_percent_float = serializers.SerializerMethodField()
    pm_red_gaps = serializers.SerializerMethodField()
    class Meta:
        model = UpGapper
        fields = ('date',
                  'creation',
                  'ticker',
                  'gap_percentage',
                  'pm_observations',
                  'last',
                  'gap_percentage_display',
                  'pm_s2_volume',
                  'pm_s1_market_cap',
                  'pm_s2_market_cap',
                  'pm_s1_float',
                  'pm_s2_float',
                  'pm_s1_held_percent_insiders',
                  'pm_s2_held_percent_insiders',
                  'pm_s1_held_percent_institutions',
                  'pm_s2_held_percent_institutions',
                  'pm_s1_short_percent_float',
                  'pm_red_gaps',
                  'company_name',
                  'industry'
                  )

    def get_last(self, obj):
        return last(obj)

    def get_gap_percentage_display(self, obj):
        return gap_percentage_display(obj)

    def get_pm_s2_volume(self, obj):
        return pm_s2_volume(obj)

    def get_pm_s1_market_cap(self, obj):
        return pm_s1_market_cap(obj)

    def get_pm_s2_market_cap(self, obj):
        return pm_s2_market_cap(obj)

    def get_pm_s1_float(self, obj):
        return pm_s1_float(obj)

    def get_pm_s2_float(self, obj):
        return pm_s2_float(obj)

    def get_pm_s1_held_percent_insiders(self, obj):
        return pm_s1_held_percent_insiders(obj)

    def get_pm_s2_held_percent_insiders(self, obj):
        return pm_s2_held_percent_insiders(obj)

    def get_pm_s1_held_percent_institutions(self, obj):
        return pm_s1_held_percent_institutions(obj)

    def get_pm_s2_held_percent_institutions(self, obj):
        return pm_s2_held_percent_institutions(obj)

    def get_pm_s1_short_percent_float(self, obj):
        return pm_s1_short_percent_float(obj)

    def get_pm_red_gaps(self, obj):
        return pm_red_gaps(obj)

class PublicGapperSerializer(serializers.ModelSerializer):
    last = serializers.SerializerMethodField()
    gap_percentage_display = serializers.SerializerMethodField()
    pm_s2_volume = serializers.SerializerMethodField()
    pm_s1_market_cap = serializers.SerializerMethodField()
    class Meta:
        model = UpGapper
        fields = ('date',
                  'ticker',
                  'gap_percentage',
                  'last',
                  'gap_percentage_display',
                  'pm_s2_volume',
                  'pm_s1_market_cap')

    def get_last(self, obj):
        return last(obj)

    def get_gap_percentage_display(self, obj):
        return gap_percentage_display(obj)

    def get_pm_s2_volume(self, obj):
        return pm_s2_volume(obj)

    def get_pm_s1_market_cap(self, obj):
        return pm_s1_market_cap(obj)
