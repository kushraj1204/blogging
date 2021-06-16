from django.db import models


# Create your models here.
class Settings(models.Model):
    page_limit = models.IntegerField(default=10)
    google_maps_api_key = models.TextField(unique=True, max_length=200)
    metakey = models.TextField(blank=True, null=True, verbose_name='Homepage Meta Key')
    metadesc = models.TextField(blank=True, null=True, verbose_name='Homepage Meta Description')

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
