import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from NewsCollector.settings import MEDIA_ROOT
from collector.forms import *
from collector.models import *

log = logging.getLogger(__name__)


def home(request):
    context = __get_basic_home_context()

    if 'action' in request.POST and request.POST['action'] == "download_museums":
        form = DownloadMuseumsForm(request.POST)
        if form.is_valid():
            form.download(file=request.FILES.get('museums_list_file'))
        else:
            log.error(form.errors.as_data())

        return redirect(f'home')

    return render(request, "home.html", context)



# def home_product_id(request, selected_product_id):
#     collector = __get_collector(request)
#     context = __get_basic_home_context(collector)
#
#     context["selected_product"] = Product.objects.get(id=selected_product_id)
#
#     return render(request, "home.html", context)


def __get_basic_home_context():
    context = dict()

    context["download_museums_form"] = DownloadMuseumsForm()
    context["media_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep
    context["museums"] = Museum.objects.values()

    context["news_list"] = News.objects.values()

    return context
