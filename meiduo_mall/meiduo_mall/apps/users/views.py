from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
# from rest_framework.request import Request
from rest_framework.generics import CreateAPIView

from users import serializers


# def index(request):
#     # return Request('index')
#     return HttpRequest('index')


# url(r'^users/$', views.UserView.as_view()),
class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer