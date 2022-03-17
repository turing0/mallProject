from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller')

    '''filter options'''
    list_filter = ('seller',)

    '''10 items per page'''
    list_per_page = 10


admin.site.register(Product, ProductAdmin)