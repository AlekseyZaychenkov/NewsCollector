from django.db import models


class Museum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=511)
    supports_wordpress_api = models.BooleanField(null=True)
    url = models.CharField(max_length=2047, null=True)


class News(models.Model):
    id = models.AutoField(primary_key=True)
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    text = models.TextField(blank=True)
    datetime = models.DateTimeField(null=True)
    link = models.CharField(max_length=2047, null=True)
