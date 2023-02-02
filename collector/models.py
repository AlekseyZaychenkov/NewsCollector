from django.db import models


class Museum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=511)
    created_with_wordpress = models.BooleanField(null=True)
    link = models.CharField(max_length=2047, null=True)


class News(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=4095)
    text = models.TextField(blank=True)
    link = models.CharField(max_length=2047, null=True)
