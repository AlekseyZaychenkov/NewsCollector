from collector.downloader import wordpress_website_authorization
from django.test import TestCase

import logging


log = logging.getLogger(__name__)


class TestDownloader(TestCase):

    def test_wordpress_website_authorization(self):
        url_1 = 'http://museumpereslavl.ru'

        wordpress_website_authorization(url_1)


