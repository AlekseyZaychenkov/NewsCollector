from django.contrib import admin
from collector.models import *


@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_with_wordpress', 'link')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass
