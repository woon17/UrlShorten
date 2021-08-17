from unittest.case import expectedFailure
from django.test import TestCase
from shortener.models import Shortener

class TestShortenerModel(TestCase):
    def test_model_str(self):
        testShortener1 = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/", random_short_url="testingOnly1")
        self.assertEqual(str(testShortener1),  "https://docs.djangoproject.com/en/3.2/: testingOnly1 - None")

        testShortener2 = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/intro/overview/", custom_short_url="testingOnly2")
        self.assertEqual(str(testShortener2),  "https://docs.djangoproject.com/en/3.2/intro/overview/: None - testingOnly2")


        testShortener3 = Shortener.objects.create(long_url="https://docs.djangoproject.com/en/3.2/topics/db/models/", random_short_url="asdfgds", custom_short_url="testingOnly3")
        self.assertEqual(str(testShortener3),  "https://docs.djangoproject.com/en/3.2/topics/db/models/: asdfgds - testingOnly3")
