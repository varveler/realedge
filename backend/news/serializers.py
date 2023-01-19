from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import News



class NewsSerializer(serializers.ModelSerializer):
    natural_time = serializers.SerializerMethodField()
    short_title = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ( 'uuid',
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
                   'natural_time',
                   'short_title')
    def get_natural_time(self, obj):
        return naturaltime(obj.publish_date)

    def get_short_title(self, obj):
        max_length = 75
        if len(obj.title) <= max_length:
            return obj.title
        return obj.title[:max_length] + '...'
