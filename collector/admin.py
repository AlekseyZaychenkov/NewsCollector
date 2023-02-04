from django.contrib import admin
from collector.models import *


@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ('name', 'supports_wordpress_api', 'url')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'museum', 'title', 'text', 'datetime', 'link')
