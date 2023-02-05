import os
import asyncio
import xml
import xmlrpc
from xmlrpc.client import ProtocolError

import urllib3
import wordpress_json

from collector.models import Museum, News

from wordpress_json import WordpressJsonWrapper
import csv
import io
import requests
from wordpress_xmlrpc import ServerConnectionError

import logging

log = logging.getLogger(__name__)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def download_museums_list(museums_list_file):
    with io.TextIOWrapper(museums_list_file) as my_file:
        read = csv.DictReader(my_file, delimiter=',')
        for row in read:
            Museum(name=row.get('_source/general/name'), url=row.get('_source/general/contacts/website')).save()


async def check_museum(museum: Museum):
    url = museum.url
    try:
        response = requests.get(f"{url}/wp-json/wp/v2/posts", timeout=0.5)

        if response.status_code == 200:
            try:
                wp = WordpressJsonWrapper(f"{url}/wp-json/wp/v2", 'wp_user', 'wp_password')
                wp.get_posts()
                museum.supports_wordpress_api = True
            except wordpress_json.WordpressError:
                log.warning(f"WordpressError: Expected JSON response but got text/html for url '{url}' ")
                museum.supports_wordpress_api = False
        elif response.status_code in {401, 403, 404, 451}:
            museum.supports_wordpress_api = False
        elif response.status_code == 500:
            log.warning(f"Error 500: Internal server error for url '{url}' ")
        elif response.status_code == 503:
            log.warning(f"Error 503: Service temporary Unavailable for url '{url}' ")
        elif response.status_code == 520:
            log.warning(f"Error 520: Web Server Is Returning an Unknown Error for url '{url}' ")
        else:
            log.warning(f"Unexpected response '{response}' for url '{url}'")
        museum.save()
    except requests.exceptions.ConnectionError:
        log.warning(f"ConnectionError exception for '{url}'")
    except requests.exceptions.TooManyRedirects:
        log.warning(f"TooManyRedirects exception for '{url}'")
    except requests.exceptions.Timeout:
        log.warning(f"Timeout exception for '{url}'")


def check_if_supports_wordpress_api(museums_list: list):
    counter = 0
    tasks = list()
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    for museum in museums_list:
        if counter % 100 == 0 and len(tasks) > 0:
            wait_tasks = asyncio.wait(tasks)
            ioloop.run_until_complete(wait_tasks)
            ioloop.close()
            log.info(f"<========== Checked '{counter}' urls ==========>")

            ioloop = asyncio.new_event_loop()
            asyncio.set_event_loop(ioloop)
            tasks = list()

        if museum.supports_wordpress_api is None:
            tasks.append(ioloop.create_task(check_museum(museum)))

        counter += 1

    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    log.info(f"<========== Checking Finished! Checked '{counter}' urls ==========>")


async def download_museum_news(museum: Museum):
    url = museum.url
    try:
        response = requests.get(f"{url}/wp-json/wp/v2/posts", timeout=0.5)
        log.info(f"For url '{url}' received response '{response}'")

        if '404' not in response.text and 'Страница не найдена' not in response.text:
            try:
                wp = WordpressJsonWrapper(f"{url}/wp-json/wp/v2", 'wp_user', 'wp_password')
                posts = wp.get_posts()
                posts = sorted(posts, key=lambda k: k['date'], reverse=True)
                news_counter = 1

                for post in posts:
                    if news_counter == 11:
                        break
                    if not post['title']['rendered'] == 'Контакты':
                        if News.objects.filter(link=post['link']).count() < 1:
                            News(museum=museum,
                                 title=post['title']['rendered'],
                                 text=post['content']['rendered'],
                                 datetime=post['date'],
                                 link=post['link']).save()
                        news_counter += 1

            except requests.exceptions.ReadTimeout:
                log.warning(f"Timeout exception for '{url}'")
            except urllib3.exceptions.ReadTimeoutError:
                log.warning(f"ReadTimeoutError exception for '{url}'")
            except wordpress_json.WordpressError:
                log.warning(f"WordpressError: Expected JSON response but got text/html for url '{url}' ")
                museum.supports_wordpress_api = False
                museum.save()
        else:
            log.warning(f"Posts from url '{url}' weren't received!")

    except ProtocolError as error:
        log.warning(f"ProtocolError for '{museum.url}' {error}")
    except ServerConnectionError as error:
        log.warning(f"ServerConnectionError for '{museum.url}' {error}")
    except xml.parsers.expat.ExpatError as error:
        log.warning(f"ExpatError for '{museum.url}' {error}")
    except xmlrpc.client.ResponseError as error:
        log.warning(f"ResponseError for '{museum.url}' {error}")


def download_news(museums_list):
    counter = 280
    tasks = list()
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)

    for museum in museums_list:
        if counter % 10 == 0 and len(tasks) > 0:
            wait_tasks = asyncio.wait(tasks)
            ioloop.run_until_complete(wait_tasks)
            ioloop.close()
            log.info(f"<==========  Downloaded news for '{counter}' museums ==========>")

            ioloop = asyncio.new_event_loop()
            asyncio.set_event_loop(ioloop)
            tasks = list()

        tasks.append(ioloop.create_task(download_museum_news(museum)))

        counter += 1

    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    log.info(f"<========== News downloading finished! Downloaded news for '{counter}' museums ==========>")
