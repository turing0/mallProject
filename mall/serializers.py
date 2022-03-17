from rest_framework import serializers
from .models import User
from .models import Product
from django.contrib.auth import get_user_model

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'balance')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'name', 'price', 'seller')

