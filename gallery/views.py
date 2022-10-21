import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ProductsAnalyzer.settings import MEDIA_ROOT
from gallery.forms import *
from gallery.models import Product

log = logging.getLogger(__name__)



def home(request):
    context = __get_basic_home_context()

    if 'action' in request.POST and request.POST['action'] == "download_posts":
        form = DownloadPostsForm(request.POST)
        if form.is_valid():
            form.download()
        else:
            log.error(form.errors.as_data())

    return render(request, "home.html", context)



# def home_product_id(request, selected_product_id):
#     gallery = __get_gallery(request)
#     context = __get_basic_home_context(gallery)
#
#     context["selected_product"] = Product.objects.get(id=selected_product_id)
#
#     return render(request, "home.html", context)


def __get_basic_home_context():
    context = dict()

    context["download_posts_form"] = DownloadPostsForm()
    context["media_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep
    context["products"] = Product.objects.values()

    return context
