from django.db import models
from reusers.models import ReUser as User
import uuid

# Create your models here.
class TradesTickerLog(models.Model):
    class Meta:
        unique_together = ('ticker', 'date', 'user')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()


# class DayLog(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#     creation = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     date = models.DateField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comments = models.TextField()
