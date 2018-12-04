from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
# from rest_framework.request import Request


def index(request):
    # return Request('index')
    return HttpRequest('index')