from bs4 import BeautifulSoup
import requests
import collections

from gallery.models import Product
import re
import logging

log = logging.getLogger(__name__)
collections.Callable = collections.abc.Callable


class Downloader:

    def download(self):
        first_page_url = "https://azbykamebeli.ru/catalog/0000057/"
        last_page_number = Downloader.__get_last_page_number(first_page_url)

        for page_num in range(1, last_page_number + 1):
            log.info(f"Start scraping page №'{page_num}'")

            if page_num == 1:
                url = f"https://azbykamebeli.ru/catalog/0000057/"
            else:
                url = f"https://azbykamebeli.ru/catalog/0000057/?page={page_num}"

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            product_list = soup.find_all('div', {'itemtype': 'http://schema.org/Product'})

            for product in product_list:
                description = product.find('div', {'class': 'item__description'})

                name = description.find('span', {'itemprop': 'name'})
                if not name:
                    log.error("Name was not parsed. Check website html structure!")
                else:
                    name = name.text

                vendor_code = description.find('small', {'class': 'text-muted f-XS'})
                if 'Артикул:' not in vendor_code.text:
                    log.error("Vendor code was not parsed. Check website html structure!")
                else:
                    vendor_code = vendor_code.text.replace('Артикул:', '').strip()

                regex = re.compile('f-XS d-inline-block badge badge-pill.*')
                availability = description.find('small', {'class': regex})
                if availability.text not in ['под заказ', 'доступно', 'в пути']:
                    log.error("Availability was not parsed. Check website html structure!")
                else:
                    availability = availability.text

                prices = product.find('div', {'class': 'item__footer mt-auto'}).find('div', {'class': 'price'})
                regex = re.compile('online-price.*')
                online_price = prices.find('div', {'class': regex})
                if online_price:
                    online_price = online_price.text[:-2].replace(' ', '')
                regex = re.compile('store-price.*')
                store_price = prices.find('a', {'class': regex})
                if store_price:
                    store_price = store_price.text[:-2].replace(' ', '')
                else:
                    store_price = online_price


                if not (store_price or online_price):
                    log.error("Prices was not parsed. Check website html structure!")

                hidden_info = product.find('div', {'class': 'item__footer_buy mt-auto'})\
                    .find('div', {'class': 'btn btn-info btn-block buyoneclick mt-1'})
                id_from_source = 0
                if 'data-id' in hidden_info.attrs:
                    id_from_source = hidden_info.attrs['data-id']
                else:
                    log.error("Id from source was not parsed. Check website html structure!")

                product_db = Product(
                    name=name,
                    vendor_code=vendor_code,
                    price=store_price,
                    price_with_discount=online_price,
                    availability=availability,
                    id_from_source=id_from_source
                )
                product_db.save()


    @staticmethod
    def __get_last_page_number(first_page_url):
        log.info("Looking for number pages for scraping...")
        page = requests.get(first_page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        paginator_list = soup.find_all('li', {'class': 'page-item'})

        last_page_number = 0
        for paginator_item in paginator_list:
            if paginator_item.text.isdigit() and int(paginator_item.text) > last_page_number:
                last_page_number = int(paginator_item.text)

        if last_page_number == 0:
            log.warning(f"Paginator for counting pages was not found! Availability and website html structure!")
        else:
            log.info(f"'{last_page_number}' pages were found")
        return last_page_number
