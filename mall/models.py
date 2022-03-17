from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# User = get_user_model()


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名', help_text='用户名')
    password = models.CharField(max_length=256, verbose_name='密码', help_text='密码')
    balance = models.FloatField(default=1000)

    # class Meta:
    #     verbose_name = '用户'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Product(models.Model):
    """Products Model"""

    name = models.CharField(max_length=90, db_index=True)
    price = models.FloatField()
    # attachment = models.FileField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_products_seller')
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_products_buyer')
    sell_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.name + ', ' + str(self.price)

