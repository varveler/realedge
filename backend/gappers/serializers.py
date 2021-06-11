from .models import UpGapper
from rest_framework import serializers



from django.contrib.humanize.templatetags.humanize import naturaltime



class GapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpGapper
        fields = (
                    'creation',
                    'update',
                    'ticker',
                    'company_name',
                    'industry',
                    'pm_source1',
                    'pm_s1_volume',
                    'pm_s1_market_cap',
                    'pm_s1_shares_outstanding',
                    'pm_s1_float',
                    'pm_s1_held_percent_insiders',
                    'pm_s1_held_percent_institutions',
                    'pm_s1_short_percent_float',
                    'pm_s1_shares_short',
                    'pm_s1_beta',
                    'pm_source2',
                    'pm_s2_volume',
                    'pm_s2_market_cap',
                    'pm_s2_shares_outstanding',
                    'pm_s2_float',
                    'pm_s2_held_percent_insiders',
                    'pm_s2_held_percent_institutions',
                    'pm_s2_short_percent_float',
                    'pm_s2_shares_short',
                    'pm_atr',
                    'pm_red_gaps',
                    'pm_observations',
        )
