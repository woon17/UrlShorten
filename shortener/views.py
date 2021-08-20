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

def index(request):
    print(request)
    return render(request, 'shortener/home.html', {"domains": getDomains()})

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


def apiGetShortUrl(request, longUrl, customShortUrl):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    try:
        longUrl = sanitizerService.sanitize(longUrl)
        customShortUrl =customShortUrl.replace("tag", "")
        customShortUrl = sanitizerService.sanitize(customShortUrl)
        print(f'longUrl: {longUrl}; customShortUrl: {customShortUrl};\n\n')
        context = {"longUrl": longUrl, "customShortUrl": customShortUrl, "domains": getDomains(), "domain": getHomeDomain()}

        if longUrl == "" or longUrl is None:
            return render(request, 'shortener/home.html', context)
        else:
            shortenerObj=Shortener.objects.filter(long_url=longUrl)
            if shortenerObj.exists() and shortenerObj[0].custom_short_url == customShortUrl:
                context["randomShortPart"]=shortenerObj[0].random_short_url
                context["customShortPart"]=shortenerObj[0].custom_short_url
                return render(request, 'shortener/home.html', context)
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
        context["errorMessage"]="Please provide a different customize input."
        return JsonResponse({'success':'true', 'context':context})

    print("success")
    context["errorMessage"]="none"

    return JsonResponse({'success':'true', 'context':context})


def apiGetLongUrl(request, shortened_part):
    response_data = []
    try:
        data={}
        if (Shortener.objects.filter(random_short_url=shortened_part).exists()):
            shortener = Shortener.objects.get(random_short_url=shortened_part)
        else:
            shortener = Shortener.objects.get(custom_short_url=shortened_part)
        data["long_url"]=shortener.long_url
        data["shortened_part"]=shortener.long_url
        response_data.append(data)
        
    except Shortener.DoesNotExist:
        # raise Http404('This shorten_url does not exist')
        print("hrtr")
        return JsonResponse({'success':'false'}, status=400)
        # return render(request, "shortener/pageNotFound.html", {"domain": getHomeDomain()})
    
    # return HttpResponseRedirect(shortener.long_url)
    print("success")
    return JsonResponse({'success':'true', 'data':response_data})