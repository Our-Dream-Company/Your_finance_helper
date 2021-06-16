from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h4>Проверка работы</h4>')


def about(request):
    return HttpResponse('<h4>Страница про нас</h4>')


def planer(request):
    return HttpResponse('<h4>Планировщик</h4>')


def invest(request):
    return HttpResponse('<h4>Портфели</h4>')
