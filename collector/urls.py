from django.urls import path

from collector.views import *


urlpatterns = [
    path('', home, name="home"),
    path('download_news', download_news_view, name="download_news"),
    path('home_show_news_by_query?q=<str:q>', home, name="home_show_news_by_query"),
    path('q=<str:q>', get_news, name="get_news"),
]
