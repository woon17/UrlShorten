from django.test import TestCase
from shortener.shortenService import createRandomShortenPart, saveShortener, updateShortener
from shortener.models import Shortener

class TestShortenService(TestCase):
    def setUp(self):
        self.newLongUrl = "https://www.djangoproject.com/download/"
        self.newCustomShortUrl = "download"
        self.newRandomShortUrl = createRandomShortenPart()

        self.testShortener = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/topics/db/models/", short_url="asdfgds", custom_short_url="testingOnly")
        self.testShortenerNoRandomShortUrl = Shortener.objects.create(long_url="https://www.djangoproject.com/weblog/", short_url=None, custom_short_url="weblog")
        self.testShortenerNoCustomShortUrl = Shortener.objects.create(long_url="https://www.djangoproject.com/start/overview/", short_url="hgfdh", custom_short_url=None)

    def test_createRandomShortenPart(self):
        random1 = createRandomShortenPart()
        random2 = createRandomShortenPart()
        self.assertNotEquals(random1, random2)
    
    def test_saveShortener(self):
        self.assertFalse(Shortener.objects.filter(long_url=self.newLongUrl).exists())
        saveShortener(self.newLongUrl, shortUrl=self.newRandomShortUrl)
        self.assertTrue(Shortener.objects.filter(long_url=self.newLongUrl).exists())
        Shortener.objects.get(long_url=self.newLongUrl).delete()

        self.assertFalse(Shortener.objects.filter(long_url=self.newLongUrl).exists())
        saveShortener(self.newLongUrl, customShortUrl=self.newCustomShortUrl)
        self.assertTrue(Shortener.objects.filter(long_url=self.newLongUrl).exists())

    def test_updateShortener(self):
        # update short_url
        self.assertTrue(self.testShortenerNoRandomShortUrl.short_url is None)
        updateShortener(self.testShortenerNoRandomShortUrl, shortUrl=self.newRandomShortUrl)
        self.assertFalse(self.testShortenerNoRandomShortUrl.short_url is None)

        # update custom_short_url       
        self.assertTrue(self.testShortenerNoCustomShortUrl.custom_short_url is None)
        updateShortener(self.testShortenerNoCustomShortUrl, customShortUrl=self.newCustomShortUrl)
        self.assertFalse(self.testShortenerNoCustomShortUrl.custom_short_url is None)