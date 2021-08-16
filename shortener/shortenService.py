from random import choice
from .models import Shortener
from string import ascii_lowercase, digits


SHORTEN_SIZE = 10

def createRandomShortenPart():
    chars = ascii_lowercase + digits + '*!@#$%^&*()_'
    shortenPart = ''.join(choice(chars) for _ in range(SHORTEN_SIZE))
    print(shortenPart)

    if Shortener.objects.filter(short_url=shortenPart).exists():
        createRandomShortenPart()
    return shortenPart

def saveShortener(longUrl, shortUrl=None, customShortUrl=None):
    if shortUrl is not None:
        Shortener.objects.create(
            long_url=longUrl,
            short_url=shortUrl
        )
    if customShortUrl is not None:
        Shortener.objects.create(
        long_url=longUrl,
        custom_short_url=customShortUrl
    )

def updateShortener(shortener, shortUrl=None, customShortUrl=None):
    if shortUrl is not None:
        shortener.short_url=shortUrl
    if customShortUrl is not None:
        shortener.custom_short_url=customShortUrl
    shortener.save()
