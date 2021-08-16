from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener
import requests, json

# Create your views here.
from django.http import HttpResponse

DOMAIN1="http://127.0.0.1:8000/"
DOMAIN2="http://localhost:8000/"

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    print("--------------------")
    try:
        print(request.body)
        longUrl = request.POST.get('longUrl')
        customShortenPart = request.POST.get('customShortenPart')
        domain = request.POST.get('domain')
        print(f'longUrl: {longUrl}; customShortenPart: {customShortenPart}; domain: {domain};')
    except:
        pass
    return render(request, 'shortener/home.html', {"longUrl": longUrl, "customShortenPart": customShortenPart, "domains": [DOMAIN1, DOMAIN2], "domain": domain})

def getLongUrl(shortenPart):
    print("------------------------")
    print("shortened_part: {}".format(shortenPart))

    try:
        shortener = Shortener.objects.get(short_url=shortenPart)
        print("long: {}".format(shortener.long_url))
    except Shortener.DoesNotExist:
        raise Http404('This shorten_url is not exist')
    return HttpResponseRedirect(shortener.long_url)
