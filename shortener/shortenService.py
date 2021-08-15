# from .models import Shortener
# from django.http import HttpResponse, Http404, HttpResponseRedirect
from random import choice
from string import ascii_lowercase, digits
import tzlocal
import pytz

SHORTEN_SIZE = 10

def getLocalCreateAt(createAt):
    local_timezone = tzlocal.get_localzone()
    return createAt.replace(tzinfo=pytz.utc).astimezone(local_timezone)


def createRandomShortenPart():
    chars = ascii_lowercase + digits + '*!@#$%^&*()_'
    shortenPart = ''.join(choice(chars) for _ in range(SHORTEN_SIZE))
    print(shortenPart)
    return shortenPart
# createRandomShortenPart()

# def getLongUrl(shortenPart):
#     print("------------------------")
#     print("shortened_part: {}".format(shortenPart))

#     try:
#         shortener = Shortener.objects.get(short_url=shortenPart)
#         print("long: {}".format(shortener.long_url))
#     except Shortener.DoesNotExist:
#         raise Http404('This shorten_url is not exist')
#     return HttpResponseRedirect(shortener.long_url)
