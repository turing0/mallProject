import pytest
from .models import User
from .models import Product
from mixer.backend.django import mixer
from django.urls import reverse


@pytest.mark.django_db
def test_user():
    assert User.objects.count() == 0
    # mixer.cycle(10).blend('User')
    User.objects.create_user(username='123456', password='123456')
    assert User.objects.get(username='123456').balance == 1000
    #  # 插入10条模拟的分类记录
    #
    #  # 插入50条模拟的文章记录
    #  mixer.cycle(50).blend('blog.Article', is_md='0', presentation='test简介')
    #  mixer.blend('blog.BlogSettings')
    #
    #  assert Category.objects.all().count() > 0
    #  assert Article.objects.all().count() > 0
    #
    # response = api_client.get('/api/products')
    # assert response.status_code == 401


@pytest.mark.django_db
def test_product():
    assert Product.objects.count() == 0
    Product.objects.create(name='banana', price='2')
    assert Product.objects.get(name='banana').name == 'banana'
    assert not Product.objects.get(name='banana').sell_date

    # User.objects.create_user(username='123456', password='123456')
    # assert User.objects.get(username='123456').balance == 1000
