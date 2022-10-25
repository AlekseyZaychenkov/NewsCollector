import operator
import logging
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Q, Min, Max

from gallery.models import Product

log = logging.getLogger(__name__)


class DiagramBuilder:

    def draw(self):
        self.draw_price_distribution_for_available_and_on_order('Распределение по цене (доступно в магазинах)',
                                                              'Распределение по цене (под заказ)' )
        self.draw_top_10_vendor_code_by_price('Топ 10 самых дорогих диванов')
        self.draw_number_of_unique_ids_for_available_and_on_order('Диаграмма уникальных id')

    def draw_price_distribution_for_available_and_on_order(self, available_diagram_name, on_order_diagram_name):
        products_count = Product.objects.count()
        log.info(f"Products count: {products_count}")

        products = Product.objects.filter(Q(availability='под заказ') | Q(availability='доступно'))

        products_min_price = int(products.aggregate(Min('price'))['price__min'])
        products_max_price = int(products.aggregate(Max('price'))['price__max'])
        x_col_nums = 20
        price_step = (products_max_price - products_min_price) // x_col_nums

        products_available_per_price = dict()
        products_available = Product.objects.filter(availability='доступно')
        for step in range(0, x_col_nums):
            price = round(products_min_price + step*price_step)
            products_available_per_price[price] = 0
            for product in products_available:
                if price - price_step // 2 < int(product.price.amount) < price + price_step // 2:
                    products_available_per_price[price] += 1
        print(f"products_available_per_price: {products_available_per_price}")

        products_on_order_per_price = dict()
        products_on_order = Product.objects.filter(availability='под заказ')
        for step in range(0, x_col_nums):
            price = round(products_min_price + step*price_step)
            products_on_order_per_price[price] = 0
            for product in products_on_order:
                if price - price_step // 2 < int(product.price.amount) < price + price_step // 2:
                    products_on_order_per_price[price] += 1
        log.info(f"products_on_order_per_price: {products_on_order_per_price}")


        df = pd.DataFrame({'Цена': products_available_per_price.keys(),
                           'количество позиций': products_available_per_price.values()
                           })
        df.plot(kind='line',
                x='Цена',
                y='количество позиций',
                color='green')
        plt.title(available_diagram_name)

        plt.savefig(f'{available_diagram_name}.png')


        df = pd.DataFrame({'Цена': products_on_order_per_price.keys(),
                           'количество позиций': products_on_order_per_price.values()
                           })
        df.plot(kind='line',
                x='Цена',
                y='количество позиций',
                color='yellow')
        plt.title(on_order_diagram_name)

        plt.savefig(f'{on_order_diagram_name}.png')

    def draw_top_10_vendor_code_by_price(self, diagram_name):
        products_top_10 = Product.objects.order_by('-price')[:10]
        products_top_10 = sorted(products_top_10, key=operator.attrgetter('price'))

        products_top_10_prices = dict()
        for product in products_top_10:
            products_top_10_prices[product.vendor_code] = int(product.price.amount)

        log.info(f"10 products with biggest price: {products_top_10_prices}")

        df = pd.DataFrame({'Артикул': products_top_10_prices.keys(),
                           'Цена': products_top_10_prices.values()
                           })
        df.plot(kind='bar',
                x='Артикул',
                y='Цена',
                color='green')
        plt.title(diagram_name)

        plt.savefig(f'{diagram_name}png')

    def draw_number_of_unique_ids_for_available_and_on_order(self, diagram_name):
        products_available_num = Product.objects.filter(availability='доступно').count()
        products_on_order_num = Product.objects.filter(availability='под заказ').count()
        log.info(f"products_available_num: {products_available_num}\nproducts_on_order_num: {products_on_order_num}")

        fig, ax = plt.subplots()
        ax.pie([products_available_num, products_on_order_num], labels=["Доступно", "Под заказ"], autopct='%1.2d%%')
        ax.axis("equal")
        ax.legend(loc='best')

        plt.title(diagram_name)

        fig.savefig(diagram_name)
