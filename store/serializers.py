from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

# class ProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Product
#         fields = ('__all__')

class PurchaseSerializer(serializers.ModelSerializer):

    product_list = serializers.SerializerMethodField(read_only=True)

    def get_product_list(self, data):
        product_list = getattr(data, 'product_list')
        print('product_list=', product_list)
        #last_purches = Transaction.objects.filter(purchase__user=product_list).last()
        return product_list

    class Meta:
        model = Purchase
        fields = ('product_list',)

class TransactionSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='purchase.user')
    email = serializers.CharField(source='purchase.user.email')
    purchase = PurchaseSerializer()
    class Meta:
        model = Transaction
        fields = ('user_name', 'email', 'time_creation', 'purchase')

class UserSerializer(serializers.ModelSerializer):

    #Дополнительне поле для вывода даты последней покупки пользователя
    last_purches = serializers.SerializerMethodField(read_only=True)

    def get_last_purches(self, data): #data приходит из views.py
        username = getattr(data, 'id')
        last_purches = Transaction.objects.filter(purchase__user=username).last()
        return last_purches.time_creation

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'date_joined', 'last_purches')


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()