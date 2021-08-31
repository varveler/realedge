from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import News



class NewsSerializer(serializers.ModelSerializer):
    natural_time = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = [ 'uuid',
                   'creation',
                   'update',
                   'internal_source',
                   'publish_date',
                   'publish_time_epoc',
                   'source',
                   'title',
                   'body',
                   'summary',
                   'tickers',
                   'url',
                   'str_date',
                   'natural_time']
    def get_natural_time(self, obj):
        return naturaltime(obj.publish_date)
