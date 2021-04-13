import csv
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from urllib.parse import urlencode


def index(request):
    return redirect(reverse(bus_stations))


def stations_pagination():
    result = []
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as f:
        dictreader = csv.DictReader(f)
        for str in dictreader:
            result.append(str)
    paginator = Paginator(result, settings.PAGINATION_PER_PAGE)
    return paginator


def bus_stations(request):
    paginator = stations_pagination()
    current_page = paginator.get_page(request.GET.get('page', '1'))
    if current_page.has_previous():
        prev_page_url = f'{reverse(bus_stations)}?' \
                        f'{urlencode({"page": current_page.previous_page_number()})}'
    else:
        prev_page_url = None
    if current_page.has_next():
        next_page_url = f'{reverse(bus_stations)}?' \
                        f'{urlencode({"page": current_page.next_page_number()})}'
    else:
        next_page_url = None
    return render(request, 'index.html', context={
        'bus_stations': current_page.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

