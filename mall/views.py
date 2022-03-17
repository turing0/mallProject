from rest_framework.views import APIView
from django.http import Http404
from .models import Product
from .models import User
from .serializers import ProductSerializer
from .serializers import UserSerializer
from rest_framework import status, exceptions
from rest_framework import generics
from rest_framework import permissions
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
import uuid
from django.core.cache import cache
from rest_framework.response import Response


class UserRegister(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            if username not in User.objects.all():
                password = serializer.data.get('password')
                user = User.objects.create(username=username, password=password)
                data = {
                    'username': user.username,
                    'password': user.password,
                    'balance': user.balance,

                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                # 获取唯一标识码
                token = uuid.uuid4().hex
                # 登陆后会将标识码存入缓存
                # cache.set(键, 值)
                cache.set(token, user.username)
                data = {
                    'msg': '登录成功',
                    'status': 200,
                    'token': token,
                }
                return Response(data)
            else:
                # 认证失败
                raise exceptions.AuthenticationFailed
        # 如果没有找到对应的用户，抛出异常
        except User.DoesNotExist:
            raise exceptions.NotFound


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # 注意：手动将 request.user 与 seller 绑定
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    """
    Retrieve, update or delete an article instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
