from django.test import TestCase
from datetime import datetime
from shortener.util import getLocalCreateAt

class TestUtil(TestCase):
    def test_getLocalCreateAt(self):
        nowLocal = datetime.now()
        nowUtc = datetime.utcnow()
        current_time_local = nowLocal.strftime("%H:%M:%S")
        self.assertEqual(getLocalCreateAt(nowUtc).strftime("%H:%M:%S"), current_time_local)