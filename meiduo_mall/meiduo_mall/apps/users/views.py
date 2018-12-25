from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
# from rest_framework.request import Request
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import constants
from users import serializers
from goods.models import SKU


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
    serializer_class = serializers.UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 返回当前请求的用户
        # 在类视图对象中，可以通过类视图对象的属性获取request
        # 在django的请求request对象中，user属性表明当前请求的用户
        return self.request.user


# PUT  /email/
class EmailView(UpdateAPIView):
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return self.request.user
    # def put(self):
    #     # 获取email
    #     # 校验email
    #     # 查询user
    #     # 更新数据
    #     # 序列化返回


# url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
class VerifyEmailView(APIView):
    """
    邮箱验证
    """
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})


class UserBrowsingHistoryView(CreateAPIView):
    """
    用户浏览历史记录
    """
    serializer_class = serializers.AddUserBrowsingHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user_id
        user_id = request.user.id


        # 查询redis
        redis_conn = get_redis_connection('history')
        sku_id_list = redis_conn.lrange('history_%s'%user_id, 0, constants.USER_BROWSE_HISTORY_MAX_LIMIT)

        # 查询1数据库
        # sku_object_list = SKU.objects.filter(id__in=sku_id_list)
        skus = []
        for sku_id in sku_id_list:
            sku = SKU.objects.get(id=sku_id)
            skus.append(sku)
        # 序列化返回
        serializer = serializers.SKUSerializer(skus, many=True)
        return Response(serializer.data)












