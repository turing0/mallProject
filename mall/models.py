from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


# User = get_user_model()


# 集成内置的user模型,并添加新的字段
class User(AbstractUser):
    balance = models.FloatField(default=1000)
    # image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.username


class Product(models.Model):
    """Products Model"""

    name = models.CharField(max_length=90, db_index=True)
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_products_owner')
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_products_buyer')
    sell_date = models.DateTimeField(auto_now_add=False, null=True)
    # attachment = models.FileField()

    def __str__(self):
        return self.name + ', ' + str(self.price)
