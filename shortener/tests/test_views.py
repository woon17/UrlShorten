from django.http import request
from django.test import TestCase
from django.urls import reverse
from shortener.models import Shortener
from shortener.util import getHomeDomain
from shortener.views import apiGetShortUrl
import json
# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.index_url = reverse('index')
        self.apiGetShortUrl = ('api/getshorturl')
        self.newLongUrl = "https://www.djangoproject.com/download/"
        self.newCustomShortUrl = "download"
        self.testShortener = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/topics/db/models/", random_short_url="asdfgds", custom_short_url="testingOnly")
        self.testShortenerNoRandomShortUrl = Shortener.objects.create(long_url="https://www.djangoproject.com/weblog/", random_short_url=None, custom_short_url="weblog")
        self.redirect_shortUrl = reverse('redirect', args=[self.testShortener.random_short_url])
        self.redirect_customUrl = reverse('redirect', args=[self.testShortener.custom_short_url])
        self.DOMAIN1 = getHomeDomain()

    # # longUrl is none 
    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    # longUrl is none 
    def test_apiGetShortUrl1(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, "", "")
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response, 
        {'success': 'true', 'context': {
            'longUrl': '', 
            'domains': ['http://127.0.0.1:8000/', 
            'http://localhost:8000/'], 
            'domain': 'http://localhost:8000/', 
            'errorMessage': 'Please provide a valid long url.'}})

    # Both longUrl and randomShortUrl are existing but customShortPart is ""
    def test_apiGetShortUrl2(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.testShortener.long_url, "")
        response =json.loads(str(response.content, encoding='utf8'))
        
        self.assertEqual(response, 
        {'success': 'true', 'context': {
            'longUrl': self.testShortener.long_url, 
            'domains': ['http://127.0.0.1:8000/', 'http://localhost:8000/'], 
            'domain': 'http://localhost:8000/', 'randomShortPart': 'asdfgds', 
            'customShortPart': 'testingOnly', 
            'errorMessage': 'none'}})
    
    # # longUrl is existing but customShortPart is "" and randomShortUrl is None
    def test_apiGetShortUrl3(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.testShortenerNoRandomShortUrl.long_url, "")
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response["context"]["longUrl"], self.testShortenerNoRandomShortUrl.long_url)
        self.assertEqual(response["context"]["domains"], ['http://127.0.0.1:8000/', 'http://localhost:8000/'])
        self.assertEqual(response["context"]["domain"], 'http://localhost:8000/')
        self.assertNotEqual(response["context"]["randomShortPart"], "")
        self.assertEqual(response["context"]["customShortPart"], self.testShortenerNoRandomShortUrl.custom_short_url)
        self.assertEqual(response["context"]["errorMessage"], 'none')

    
    # # longUrl is new but customShortPart is ""
    def test_apiGetShortUrl4(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.newLongUrl, "")
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response["context"]["longUrl"], self.newLongUrl)
        self.assertEqual(response["context"]["domains"], ['http://127.0.0.1:8000/', 'http://localhost:8000/'])
        self.assertEqual(response["context"]["domain"], 'http://localhost:8000/')
        self.assertNotEqual(response["context"]["randomShortPart"], "")
        self.assertEqual(response["context"]["customShortPart"], None)
        self.assertEqual(response["context"]["errorMessage"], 'none')


    # # Both longUrl and shortUrl are existing but customShortPart is new
    def test_apiGetShortUrl5(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.testShortener.long_url, "wen")
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response["context"]["longUrl"], self.testShortener.long_url)
        self.assertEqual(response["context"]["domains"], ['http://127.0.0.1:8000/', 'http://localhost:8000/'])
        self.assertEqual(response["context"]["domain"], 'http://localhost:8000/')
        self.assertEqual(response["context"]["randomShortPart"], "asdfgds")
        self.assertEqual(response["context"]["customShortPart"], "wen")
        self.assertEqual(response["context"]["errorMessage"], 'none')

    # longUrl is new but customShortPart is an existing
    def test_apiGetShortUrl6(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.newLongUrl, "weblog")
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response, {'success': 'true', 'context': {
            'longUrl': self.newLongUrl, 
            'domains': ['http://127.0.0.1:8000/', 'http://localhost:8000/'], 
            'domain': 'http://localhost:8000/', 
            'errorMessage': 'Please provide a different customize input.'}})

    # longUrl and customShortPart are both new (new shortenerObj)
    def test_apiGetShortUrl7(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.newLongUrl, self.newCustomShortUrl)
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response, {'success': 'true', 'context': {
            'longUrl': self.newLongUrl, 
            'domains': ['http://127.0.0.1:8000/', 'http://localhost:8000/'], 
            'domain': 'http://localhost:8000/', 
            'randomShortPart': None, 
            'customShortPart': self.newCustomShortUrl, 
            'errorMessage': 'none'}})

    # longUrl and customShortPart are both existing, randomShortUrl is existing
    def test_apiGetShortUrl8(self):
        request = self.client.post(self.apiGetShortUrl)
        response = apiGetShortUrl(request, self.testShortener.long_url, self.testShortener.custom_short_url)
        response =json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(response, {'success': 'true', 'context': {
            'longUrl': self.testShortener.long_url, 
            'domains': ['http://127.0.0.1:8000/', 'http://localhost:8000/'], 
            'domain': 'http://localhost:8000/', 
            'randomShortPart': self.testShortener.random_short_url, 
            'customShortPart': self.testShortener.custom_short_url, 
            'errorMessage': 'none'}})

    def test_redirectUrlview_shortUrl(self):
        # success_redirect by random_short_url
        response = self.client.get(self.redirect_shortUrl)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "shortener/base.html")
        self.assertTemplateNotUsed(response, "shortener/home.html")
        self.assertTemplateNotUsed(response, "shortener/pageNotFound.html")

        # success_redirect by custom_short_url
        response = self.client.get(self.redirect_customUrl)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "shortener/base.html")
        self.assertTemplateNotUsed(response, "shortener/home.html")
        self.assertTemplateNotUsed(response, "shortener/pageNotFound.html")

        # fail_redirect due to no-existing data
        response = self.client.get("/notexisting/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/pageNotFound.html")
