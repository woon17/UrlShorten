from django.test import TestCase
from mysite.sanitizerService import sanitize

class TestUtil(TestCase):
    def test_sanitize(self):
        self.assertEqual(sanitize("!@#$%^&*()_+{}:<>?'"), "!@$^*_")
