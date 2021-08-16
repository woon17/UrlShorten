# from .models import Shortener
# from django.http import HttpResponse, Http404, HttpResponseRedirect
from random import choice
import shortener
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

# def getLongUrl(shortenPart):
#     print("------------------------")
#     print("shortened_part: {}".format(shortenPart))

#     try:
#         shortener = Shortener.objects.get(short_url=shortenPart)
#         print("long: {}".format(shortener.long_url))
#     except Shortener.DoesNotExist:
#         raise Http404('This shorten_url is not exist')
#     return HttpResponseRedirect(shortener.long_url)
