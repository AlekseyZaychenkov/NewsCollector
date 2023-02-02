from django.urls import path

from collector.views import home


urlpatterns = [
    path('', home, name="home"),
]
