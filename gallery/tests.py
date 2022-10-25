import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProductsAnalyzer.settings")
import django
django.setup()

from django.test import TestCase

from gallery.downloader import Downloader
from gallery.models import Product
from  gallery.diagram_builder import DiagramBuilder
import logging

log = logging.getLogger(__name__)

class TestDownloader(TestCase):

    def test_download(self):
        Product.objects.all().delete()

        downloader = Downloader()

        downloader.download()

        products = Product.objects.all()
        products = sorted(products, key=lambda prod: getattr(prod, 'id_from_source'), reverse=True)

        log.info("Products:")
        for p in products:
            log.info(f"<===== ===== ===== p.id: {p.id} ===== ===== =====>")
            log.info(f"p.name: {p.name}")
            log.info(f"p.vendor_code: {p.vendor_code}")
            log.info(f"p.price: {p.price}")
            log.info(f"p.price_with_discount: {p.price_with_discount}")
            log.info(f"p.availability: {p.availability}")
            log.info(f"p.id_from_source: {p.id_from_source}")


class TestDiagramBuilder(TestCase):

    def test_diagram_builder(self):
        builder = DiagramBuilder()

        builder.draw()
