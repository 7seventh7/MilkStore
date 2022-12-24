from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    #Дополнительне поле для вывода даты последней покупки пользователя
    last_purches = serializers.SerializerMethodField(read_only=True)

    def get_last_purches(self, data): #data приходит из views.py
        username = getattr(data, 'id')
        # пример обращения к связанной purchase талбице через foreinkey (purchase__use)
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