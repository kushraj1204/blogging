from django.db import models


# Create your models here.
class Settings(models.Model):
    page_limit = models.IntegerField(default=10)
    google_maps_api_key = models.TextField(unique=True, max_length=200)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
