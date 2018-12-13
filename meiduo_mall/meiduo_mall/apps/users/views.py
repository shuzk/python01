from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
# from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users import serializers


# def index(request):
#     # return Request('index')
#     return HttpRequest('index')


# url(r'^users/$', views.UserView.as_view()),
from users.models import User


class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


# GET /user/
class UserDetailView(RetrieveAPIView):
    """用户基本信息"""
    serializers_class = serializers.UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 返回当前请求的用户
        # 在类视图对象中，可以通过类视图对象的属性获取request
        # 在django的请求request对象中，user属性表明当前请求的用户
        return self.request.user




