import os

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from NewsCollector.settings import MEDIA_ROOT
from collector.downloader import check_if_supports_wordpress_api, download_news
from collector.forms import *
from collector.models import *

log = logging.getLogger(__name__)


def home(request, q: str = None):

    if 'action' in request.POST:
        if request.POST['action'] == "download_museums":
            form = DownloadMuseumsForm(request.POST)
            if form.is_valid():
                form.download(file=request.FILES.get('museums_list_file'))
                museums = Museum.objects.all()
                check_if_supports_wordpress_api(museums)
            else:
                log.error(form.errors.as_data())

            return redirect(f'home')

        if request.POST['action'] == "find_news_by_query":
            form = FindNewsByQueryForm(request.POST)
            if form.is_valid():
                q = form.get_query()
            else:
                log.error(form.errors.as_data())

            return redirect(f'home_show_news_by_query', q=q)

    context = __get_home_context(q)
    return render(request, "home.html", context)


def download_news_view(request):
    museums_list = Museum.objects.filter(supports_wordpress_api=True)
    download_news(museums_list)
    return redirect(f'home')


def __get_home_context(q: str = None):
    context = dict()

    context["download_museums_form"] = DownloadMuseumsForm()
    context["find_news_by_query_form"] = FindNewsByQueryForm()

    context["media_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep
    context["museums_counter"] = Museum.objects.count()
    context["museums_wordpress_counter"] = Museum.objects.filter(supports_wordpress_api=True).count()
    context["museums_not_wordpress_counter"] = Museum.objects.filter(supports_wordpress_api=False).count()
    context["museums_not_wordpress_defined_counter"] = Museum.objects.filter(supports_wordpress_api=None).count()

    if q:
        context["news_list"] = News.objects \
                                   .filter(Q(title__icontains=q) | Q(text__icontains=q)) \
                                   .order_by('datetime') \
                                   .all()[:10]

    return context


def get_news(request, q: str = None):
    news = News.objects \
               .filter(Q(title__icontains=q) | Q(text__icontains=q)) \
               .order_by('datetime') \
               .all()[:10] \
               .values('title', 'text', 'link')
    news_list = list(news)
    return JsonResponse(news_list, safe=False)
