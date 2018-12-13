from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.models import OAuthQQUser
from oauth.utils import OAuthQQ
from oauth.exceptions import OAuthQQAPIError


#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """
    # 获取QQ登录的url
    """
    def get(self, request):
        """
        提供用于qq登录的url
        """
        next = request.query_params.get('next')
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()
        return Response({'login_url': login_url})


class QQAuthUserView(APIView):

    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 凭借code 获取access_token
        oauth_qq = OAuthQQ()
        try:
            access_token = oauth_qq.get_access_token(code)
            openid = oauth_qq.get_openid(access_token)
        except OAuthQQAPIError:
            return Response({'message': '获取access_token和openid失败，即访问qq接口失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid查询数据库OAuthQQUser  判断数据时否存在
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果数据不存在，处理openid并返回
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({'access_token': access_token})
        else:
            # 如果数据存在，表示用户已经绑定过身份，签发JWT token
            # 签发JWT token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            user = oauth_qq_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({
                'username': user.username,
                'user_id': user.id,
                'token': token
            })







