import urllib.parse
from urllib.parse import urlencode

from django.conf import settings

from urllib.parse import urlencode, parse_qs
# from urllib.request import urlopen
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
import json
import logging

# from . import constants

logger = logging.getLogger('django')


class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """
    def __init__(self, client_id=None, redirect_uri=None, state=None):
        self.client_id = client_id or settings.QQ_CLIENT_ID
        # self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径

    def get_qq_login_url(self):
        """
        获取qq登录的网址
        :return: url网址
        """
        # url = 'https://graph.qq.com/oauth2.0/authorize?'
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            # 'scope': 'get_user_info',
        }
        url += urllib.parse.urlencode(params)
        return url
