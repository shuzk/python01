
from haystack import indexes

from goods.models import SKU

class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 作用
    # 1.明确在索引引擎中索引数据包含哪些字段
    # 2.字段也会作为前端进行检索查询时关键词的参数名

    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.CharField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        # return SKU.objects.filter(is_launched=True)
        return self.get_model().objects.filter(is_launched=True)






