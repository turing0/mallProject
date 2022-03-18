from rest_framework.views import APIView
from django.http import Http404
from .models import Product
from .models import User
from .serializers import ProductSerializer
from .serializers import UserSerializer
from rest_framework import status, exceptions
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import uuid
from django.core.cache import cache
from rest_framework.response import Response
from django_filters import rest_framework
from rest_framework import viewsets


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
    # authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        user = User.objects.get(username=request.user)
        if user.balance > 0:
            return Response(serializer.data)
        data = {
            'error': 'Insufficient balance! '
        }
        return Response(data)
        # return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        # serializer = ProductSerializer(data=request.data, context={"seller": user})
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            # 注意：手动将 request.user 与 seller 绑定
            serializer.save(owner=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone #引入timezone模块
class ProductBuy(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        user = User.objects.get(username=request.user)
        if user.balance > 0:
            return Response(serializer.data)
        data = {
            'error': 'Insufficient balance! '
        }
        return Response(data)
        # return Response(serializer.data)

    def post(self, request, format=None):
        product_id = request.data.get('id')
        # user = request.user
        user = User.objects.get(username=request.user)
        product = Product.objects.get(id=product_id)

        if product.buyer:
            return Response({'error': "This product has been bought."})
        if str(user) == product.owner:
            return Response({'error': "Can't buy own stuff!"})

        if user.balance >= product.price:

            user.balance -= product.price
            user.save()
            seller_user = User.objects.get(username=product.owner)
            seller_user.balance += product.price
            seller_user.save()

            data = {
                'name': product.name,
                'price': product.price,
                'owner': str(user.username),
                'buyer': str(user.username),
                'sell_date': timezone.now()
            }

            serializer = ProductSerializer(instance=product, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        data = {
            'error': 'Insufficient balance! '
        }
        return Response(data)

        data = {
            'id': product_id,
            'u': str(user),
            'p': str(product.owner),
            'date': str(sell_date)
        }
        # serializer = ProductSerializer(data=request.data, context={"seller": user})
        # serializer = ProductSerializer(data=request.data)
        return Response(data)
        if serializer.is_valid():
            # 注意：手动将 request.user 与 seller 绑定
            serializer.save(owner=request.user)
            # serializer.save()
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


class OrderList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = {'sell_date': ['isnull']}
    # filterset_fields = {
    #     # 'buyer': ['isnull']
    #     'name': ['香蕉']
    # }

        # # products = Product.objects.filter(buyer__isnull=True)
        # products = Product.objects.all()
        # filter_backends = (rest_framework.DjangoFilterBackend,)
        # filterset_fields = {
        #     'buyer': ['isnull']
        # }
        # serializer = ProductSerializer(data=products, many=True)
        #
        # # queryset = Product.objects.filter(buyer__isnull=True)
        # # serializer = ProductSerializer(data=products, many=True)
        # # data = {
        # #     'res': len(products)
        # # }
        # # return Response(data)
        # if serializer.is_valid():
        #     return Response(serializer.data)
        # #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # def post(self, request, format=None):
    #     user = request.user
    #     # serializer = ProductSerializer(data=request.data, context={"seller": user})
    #     serializer = ProductSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         # 注意：手动将 request.user 与 seller 绑定
    #         serializer.save(owner=request.user)
    #         # serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)