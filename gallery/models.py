import os

from django.db import models
from djmoney.models.fields import MoneyField
from django.dispatch import receiver


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    vendor_code = models.CharField(max_length=512, null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', null=True)
    price_with_discount = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', null=True)

    AVAILABILITIES = (
        ('доступно', 'доступно'),
        ('под заказ', 'под заказ'),
        ('в пути', 'в пути'),
    )
    availability = models.CharField(max_length=255, choices=AVAILABILITIES, default='под заказ')
    id_from_source = models.IntegerField()

