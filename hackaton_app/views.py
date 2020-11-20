from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User


def home(request):
    context = {'title': 'Strona Główna'}
    return render(request, 'hackaton_app/home.html', context)


