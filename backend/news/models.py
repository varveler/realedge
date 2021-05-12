from django.db import models
from gappers.models import UpGapper, DownGapper

import uuid

# Create your models here.
class News(models.Model):
    """ News article that relates to a certain tickers. """

    class Meta:
        unique_together = ['internal_source', 'title']
        ordering = ['-publish_date', 'title']

    # internaly created
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    internal_source = models.CharField(max_length=50) # newsApi #stockNews #scraping Finviz #scraping Benzinga #etc

    # provided externally
    publish_date = models.DateTimeField()
    publish_time_epoc = models.BigIntegerField(null=True)
    source = models.CharField(max_length=100)
    title = models.TextField()
    body = models.TextField(blank=True)
    summary = models.TextField(blank=True) #description
    tickers = models.CharField(max_length=400)
    author = models.CharField(max_length=200, blank=True)

    url = models.URLField(max_length=900)
    img_url = models.URLField(max_length=900)

    gmtOffSetMilliseconds = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)

    # relationships
    up_gapper = models.ManyToManyField(UpGapper, null=True, blank=True)
    down_gapper = models.ManyToManyField(DownGapper, null=True, blank=True)

    def __str__(self):
        return '{internal_source} {publish_date} {title} {url}'.format(
                                        internal_source = self.internal_source,
                                        publish_date = self.publish_date,
                                        title = self.title,
                                        url = self.url)
