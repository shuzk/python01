from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from goods.serializers import SKUSerializer
from goods.models import SKU

# Create your views here.


class SKUListView(ListAPIView):
    """
    商品列表视图
    """
    serializer_class = SKUSerializer

    # 排序
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'price', 'sales')

    # 分页,全局设置

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id, is_launched=True)




