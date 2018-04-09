from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blogApp.models import Article,Category

import markdown2
# Create your views here.

class IndexView(ListView):
    """
    首页视图 继承ListView ,用于展示从数据库中获取的文章列表

    """
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = "blog/index.html"
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = "article_list"
    def get_queryset(self):
        """
        过滤数据，获取所有已发布的文章，并且将内容转成markdown 形式

        """
    # 获取数据库中的所有已发布的文章，即filter(过滤)状态为'p'(已发布)的文章。
        article_list = Article.objects.filter(status='p')
        for article in article_list:
        # 将markdown标记的文本转为html文本
            article.body = markdown2.markdown(article.body)
        return article_list

    def get_context_data(self, **kwargs):
        # 增加额外的数据，这里返回一个文章分类，以字典的形式
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView,self).get_context_data(**kwargs)




################################################


class ArticleDetailView(DetailView):
    # Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    model = Article
    # 指定视图获取哪个model

    template_name = "blog/detail.html"
    # 指定要渲染的模板文件

    context_object_name = "article"
    # 在模板中需要使用的上下文名字

    pk_url_kwarg = 'article_id'

    # 这里注意，pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id

    # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body)
        return obj



################################################


class CategoryView(ListView):
    # 继承自ListView,用于展示一个列表

    template_name = "blog/index.html"
    # 指定需要渲染的模板

    context_object_name = "article_list"

    # 指定模板中需要使用的上下文对象的名字

    def get_queryset(self):
        # get_queryset 的作用已在第一篇中有介绍，不再赘述
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        # 注意在url里我们捕获了分类的id作为关键字参数（cate_id）传递给了CategoryView，传递的参数在kwargs属性中获取。
        for article in article_list:
            article.body = markdown2.markdown(article.body, )
        return article_list

    # 给视图增加额外的数据
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        # 增加一个category_list,用于在页面显示所有分类，按照名字排序
        return super(CategoryView, self).get_context_data(**kwargs)
