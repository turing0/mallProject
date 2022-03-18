from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    re_path(r'^products/$', views.ProductList.as_view()),
    re_path(r'^products/buy', views.ProductBuy.as_view()),
    re_path(r'^products/(?P<pk>[0-9]+)$', views.ProductDetail.as_view()),
    re_path(r'^orders/$', views.OrderList.as_view()),
    re_path(r'^register', views.UserRegister.as_view()),
    re_path(r'^login', views.UserLogin.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
