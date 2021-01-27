from django.db import models
from gappers.models import UpGapper, DownGapper

# Create your models here.
class News(models.Model):
    """
        News article that relates to a certain stock (gapper)
    """

    creation = models.DateTimeField(auto_now_add=True)
    source_id = models.CharField(max_length=400, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)

    provider_publish_time = models.DateTimeField()
    provider_publish_time_epoc = models.IntegerField()
    provider = models.CharField(max_length=100)
    scrap_source = models.CharField(max_length=50)
    url = models.URLField(max_length=600)

    title = models.CharField(max_length=800)
    body = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    tickers = models.CharField(max_length=100)
    authors = models.CharField(max_length=200, null=True, blank=True)
    gmtOffSetMilliseconds = models.IntegerField(null=True, blank=True)

    up_gapper = models.ManyToManyField(UpGapper)
    down_gapper = models.ManyToManyField(DownGapper)
