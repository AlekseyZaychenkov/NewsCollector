import collections

from collector.models import Museum
import re
import csv
import io
import requests
import base64

import logging

log = logging.getLogger(__name__)


def download_museums_list(museums_list_file):
    with io.TextIOWrapper(museums_list_file) as my_file:
        read = csv.DictReader(my_file, delimiter=',')
        for row in read:
            Museum(name=row.get('_source/general/name'), link=row.get('_source/general/contacts/website')).save()


def check_if_created_with_wordpress(museums_list_file):
    pass


def wordpress_website_authorization(url):
    wordpress_user = "your username"
    wordpress_password = "xxxx xxxx xxxx xxxx xxxx xxxx"
    wordpress_credentials = wordpress_user + ":" + wordpress_password
    wordpress_token = base64.b64encode(wordpress_credentials.encode())
    wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}

    response = requests.get(url, headers=wordpress_header)
    print(response)



def download_news(museums_list_file):
    def read_wordpress_posts():
        api_url = 'https://robingeuens.com/wp-json/wp/v2/posts'

        response = requests.get(api_url)
        response_json = response.json()

        print(response_json)



