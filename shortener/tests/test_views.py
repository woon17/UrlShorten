from django.test import TestCase
from django.urls import reverse
from shortener.models import Shortener
from shortener.views import DOMAIN1

# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.index_url = reverse('index')
        self.newLongUrl = "https://www.djangoproject.com/download/"
        self.newCustomShortUrl = "download"
        self.testShortener = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/topics/db/models/", short_url="asdfgds", custom_short_url="testingOnly")
        self.testShortenerNoRandomShortUrl = Shortener.objects.create(long_url="https://www.djangoproject.com/weblog/", short_url=None, custom_short_url="weblog")
        self.redirect_shortUrl = reverse('redirect', args=[self.testShortener.short_url])
        self.redirect_customUrl = reverse('redirect', args=[self.testShortener.custom_short_url])

    # longUrl is none 
    def test_index1(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    # Both longUrl and randomShortUrl are existing but customShortenPart is ""
    def test_index2(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.testShortener.long_url,
            "customShortenPart": "",
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")
    
    # longUrl is existing but customShortenPart is "" and randomShortUrl is None
    def test_index3(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.testShortenerNoRandomShortUrl.long_url,
            "customShortenPart": "",
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")
    
    # Both longUrl is new but customShortenPart is ""
    def test_index4(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.newLongUrl,
            "customShortenPart": "",
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    # Both longUrl is existing but customShortenPart is new
    def test_index5(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.testShortener.long_url,
            "customShortenPart": self.newCustomShortUrl,
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")


    # longUrl is new but customShortenPart is an existing
    def test_index6(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.newLongUrl,
            "customShortenPart": self.testShortener.custom_short_url,
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    # longUrl and customShortenPart are both new (new shortenerObj)
    def test_index7(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.newLongUrl,
            "customShortenPart": self.newCustomShortUrl,
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    # longUrl and customShortenPart are both existing, randomShortUrl is existing
    def test_index8(self):
        response = self.client.post(self.index_url,{
            "longUrl": self.testShortener.long_url,
            "customShortenPart": self.testShortener.custom_short_url,
            "domain": DOMAIN1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/base.html")
        self.assertTemplateUsed(response, "shortener/home.html")

    def test_redirectUrlview_shortUrl(self):
        # success_redirect by short_url
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
