from django.urls import path

from gallery.views import home


urlpatterns = [
    path('home', home, name="home"),
]
