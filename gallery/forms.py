# -*- coding: utf-8 -*-

from django import forms
import logging

from gallery.downloader import Downloader
from gallery.models import Product

log = logging.getLogger(__name__)


class DownloadPostsForm(forms.Form):
    clear_previous = forms.BooleanField(required=False)

    def download(self):
        if self.cleaned_data["clear_previous"]:
            Product.objects.all().delete()

        downloader = Downloader()
        downloader.download()
