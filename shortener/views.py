from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener
from .shortenService import createRandomShortenPart, saveShortener, updateShortener
from mysite import sanitizerService
from django.http import HttpResponse
import os
from .util import getDomains, getHomeDomain
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    domain = request.POST.get('domain', None)
    domain = sanitizerService.sanitize(domain)
    return render(request, 'shortener/home.html', {"domains": getDomains(), "domain": domain})

def redirectUrlview(request, shortened_part):
    try:
        if (Shortener.objects.filter(random_short_url=shortened_part).exists()):
            shortener = Shortener.objects.get(random_short_url=shortened_part)
        else:
            shortener = Shortener.objects.get(custom_short_url=shortened_part)
    except Shortener.DoesNotExist:
        # raise Http404('This shorten_url does not exist')
        return render(request, "shortener/pageNotFound.html", {"domain": getHomeDomain()})
    return HttpResponseRedirect(shortener.long_url)


def apiGetShortUrl(request):
    try:
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        customShortUrl = sanitizerService.sanitize(body.get('cus'))
        longUrl = body.get('long')
        print(f'longUrl: {longUrl}; customShortUrl: {customShortUrl};\n\n')
        context = {"longUrl": longUrl, "domains": getDomains(), "domain": getHomeDomain()}

        if longUrl == "" or longUrl is None:
            context["errorMessage"]="Please provide a valid long url."
            return JsonResponse({'success':'true', 'context':context})
        else:
            shortenerObj=Shortener.objects.filter(long_url=longUrl)
            if shortenerObj.exists() and shortenerObj[0].custom_short_url == customShortUrl:
                context["randomShortPart"]=shortenerObj[0].random_short_url
                context["customShortPart"]=shortenerObj[0].custom_short_url
            if shortenerObj.exists():
                if customShortUrl != "":
                    updateShortener(shortenerObj[0], customShortUrl=customShortUrl)
                else:
                    if shortenerObj[0].random_short_url is None:
                        shortenPart = createRandomShortenPart()
                        updateShortener(shortenerObj[0], shortUrl=shortenPart)
                context["randomShortPart"]=shortenerObj[0].random_short_url
                context["customShortPart"]=shortenerObj[0].custom_short_url
            else:
                if customShortUrl != "":
                    saveShortener(longUrl=longUrl, customShortUrl=customShortUrl)
                else:
                    shortenPart = createRandomShortenPart()
                    saveShortener(longUrl=longUrl, shortUrl=shortenPart)
                shortener=Shortener.objects.filter(long_url=longUrl)[0]
                context["randomShortPart"]=shortener.random_short_url
                context["customShortPart"]=shortener.custom_short_url

    except Exception as e:
        print("hrtr")
        print(f'Exception: {e}')
        context["errorMessage"]=e + "Please provide a different customize input."
        return JsonResponse({'success':'true', 'context':context})

    context["errorMessage"]="none"
    return JsonResponse({'success':'true', 'context':context})
