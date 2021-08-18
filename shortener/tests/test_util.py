from django.test import TestCase
from datetime import datetime
from shortener.util import getLocalCreateAt, getHomeDomain, getDomains
class TestUtil(TestCase):
    def test_getLocalCreateAt(self):
        nowLocal = datetime.now()
        nowUtc = datetime.utcnow()
        current_time_local = nowLocal.strftime("%H:%M:%S")
        self.assertEqual(getLocalCreateAt(nowUtc).strftime("%H:%M:%S"), current_time_local)

    def test_getHomeDomain(self):
        self.assertEqual(getHomeDomain(), "http://localhost:8000/")

    def test_getDomains(self):
        self.assertEqual(getDomains(), ["http://127.0.0.1:8000/", "http://localhost:8000/"])