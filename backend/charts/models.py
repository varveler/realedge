from django.db import models

# Create your models here.

import os

def create_path(instance, filename):
    return os.path.join(
        'data',
        'bars',
        instance.timeframe,
        instance.ticker[0].upper(),
        instance.ticker,
        filename
    )

class StockBarDataFile(models.Model):
    ONE_MINUTE = '1M'
    FIVE_MINUTE = '5M'
    HOUR = '1H'
    DAY = '1D'
    TIMEFRAME_CHOICES = [
        (ONE_MINUTE, '1M'),
        (FIVE_MINUTE, '5M'),
        (HOUR, '1Hour'),
        (DAY, '1Day')]

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    ticker = models.CharField(max_length=10)
    timeframe = models.CharField(max_length=2, choices=TIMEFRAME_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    _file = models.FileField(upload_to=create_path)
