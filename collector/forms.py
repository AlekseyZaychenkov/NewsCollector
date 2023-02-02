# -*- coding: utf-8 -*-

from django import forms
import logging

from collector.downloader import download_museums_list
from collector.models import Museum

log = logging.getLogger(__name__)


class DownloadMuseumsForm(forms.Form):
    museums_list_file = forms.FileField(required=False)
    clear_previous = forms.BooleanField(required=False)

    def download(self, file):
        data = self.cleaned_data

        if data.get('clear_previous'):
            Museum.objects.all().delete()

        # TODO: validate that file is .csv
        download_museums_list(file)
