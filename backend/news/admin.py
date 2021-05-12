from django.contrib import admin
from .models import News

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ordering = ('-publish_date',)
    list_display = (
        'internal_source',
        'publish_date',
        'source',
        'title',
        'tickers',
        'url',
    )
