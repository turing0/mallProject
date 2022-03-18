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
    # owner_name = serializers.ReadOnlyField(source="owner.username")
    # buyer_name = serializers.ReadOnlyField(source="buyer.username")

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('id', 'name', 'price', 'owner', 'buyer', 'sell_date')

    # def update(self, instance, validated_data):
    #     if validated_data.get("owner"):
    #         owner = validated_data.pop('owner')
    #         owner = Product.objects.get(id=self.initial_data["id"])
    #         owner_task = super(ProductSerializer, self, ).update(instance, validated_data)
    #         owner_task.owner = owner
    #         owner_task.save()
    #         return owner_task
    #     return super(ProductSerializer, self, ).update(instance, validated_data)
    # 处理外键字段
    # def create(self, validated_data):
    #     return Product.objects.create(seller=self.context["seller"], **validated_data)
