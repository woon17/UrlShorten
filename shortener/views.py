from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener
from .shortenService import createRandomShortenPart, saveShortener, updateShortener
from mysite import sanitizerService
from django.http import HttpResponse

from io import BytesIO

DOMAIN1="http://127.0.0.1:8000/"
DOMAIN2="http://localhost:8000/"

def index(request):
    try:
        longUrl = request.POST.get('longUrl', None)
        longUrl = sanitizerService.sanitize(longUrl)

        customShortenPart = request.POST.get('customShortenPart', None)
        customShortenPart = sanitizerService.sanitize(customShortenPart)

        domain = request.POST.get('domain', None)
        domain = sanitizerService.sanitize(domain)

        print(f'longUrl: {longUrl}; customShortenPart: {customShortenPart}; domain: {domain};\n\n')
        context = {"longUrl": longUrl, "customShortenPart": customShortenPart, "domains": [DOMAIN1, DOMAIN2], "domain": domain}

        if longUrl == "" or longUrl is None:
            return render(request, 'shortener/home.html', context)
        else:
            shortenerObj=Shortener.objects.filter(long_url=longUrl)
            if shortenerObj.exists() and shortenerObj[0].custom_short_url == customShortenPart:
                context["shortener"]=shortenerObj[0]
                return render(request, 'shortener/home.html', context)
            if shortenerObj.exists():
                if customShortenPart != "":
                    updateShortener(shortenerObj[0], customShortUrl=customShortenPart)
                else:
                    if shortenerObj[0].random_short_url is None:
                        shortenPart = createRandomShortenPart()
                        updateShortener(shortenerObj[0], shortUrl=shortenPart)
                context["shortener"]=shortenerObj[0]
            else:
                if customShortenPart != "":
                    saveShortener(longUrl=longUrl, customShortUrl=customShortenPart)
                else:
                    shortenPart = createRandomShortenPart()
                    saveShortener(longUrl=longUrl, shortUrl=shortenPart)
                context["shortener"]=Shortener.objects.filter(long_url=longUrl)[0]



    except Exception as e:
        print(f'Exception: {e}')
        context["errorMessage"]="Please provide a different customize input."


    return render(request, 'shortener/home.html', context)


def redirectUrlview(request, shortened_part):
    try:
        if (Shortener.objects.filter(random_short_url=shortened_part).exists()):
            shortener = Shortener.objects.get(random_short_url=shortened_part)
        else:
            shortener = Shortener.objects.get(custom_short_url=shortened_part)
    except Shortener.DoesNotExist:
        # raise Http404('This shorten_url does not exist')
        return render(request, "shortener/pageNotFound.html")
    return HttpResponseRedirect(shortener.long_url)