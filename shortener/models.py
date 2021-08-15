from django.db import models
from .shortenService import createRandomShortenPart, getLocalCreateAt


# Create your models here.
class Shortener(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=31, unique=True, blank=True)

    def __str__(self):
        return f'{self.long_url} to {self.short_url} at {getLocalCreateAt(self.createdAt)}'
    
    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = createRandomShortenPart(self)
        super().save(*args, **kwargs)
