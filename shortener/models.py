from django.db import models
from .util import getLocalCreateAt


# Create your models here.
class Shortener(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    long_url = models.URLField(max_length=100, unique=True, blank=True)
    random_short_url = models.CharField(max_length=10, unique=True, blank=True, null=True)
    custom_short_url = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        # return f'{self.long_url} to {self.random_short_url} at {getLocalCreateAt(self.createdAt)}'
        return f'{self.long_url}: {self.random_short_url} - {self.custom_short_url}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
