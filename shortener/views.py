from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def getLongUrl(shortenPart):
    print("------------------------")
    print("shortened_part: {}".format(shortenPart))

    try:
        shortener = Shortener.objects.get(short_url=shortenPart)
        print("long: {}".format(shortener.long_url))
    except Shortener.DoesNotExist:
        raise Http404('This shorten_url is not exist')
    return HttpResponseRedirect(shortener.long_url)
