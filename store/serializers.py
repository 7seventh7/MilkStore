from rest_framework import serializers
from .models import *
from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class PurchaseSerializer(serializers.ModelSerializer):
    # Получаем список всех товаров входящич в покупку. пример работы с Many to many !!!!! Обязательно source!!!
    # Проверяй related name в модели
    # Пример вложенного сериализатора!!!
    products = ProductSerializer(many=True, source='product_list')

    # Обращаемся к модели Юзер через ForeinKey. Чтобы имена были вместо цифр
    user = serializers.CharField(source='user.username')

    is_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'user', 'products', 'is_paid')

    # !!!!! Функция которая вичисляет оплачена покупка или нет !!!!
    # Берём id покупки и есил его нету в транзакиях, то покупка ещё не оплачена
    def get_is_paid(self, data):
        purchase_id = getattr(data, 'id')   # данные приходят в виде: data {'_state': <django.db.models.base.ModelState object at 0x7f4184992c10>, 'id': 1, 'user_id': 2}
        transaction_id = Transaction.objects.filter(purchase__id=purchase_id)
        if transaction_id:
            return True
        else:
            return False

class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='purchase.user')
    email = serializers.CharField(source='purchase.user.email')
    product = PurchaseSerializer(many=True, read_only=True, source='product_list')

    class Meta:
        model = Transaction
        fields = ('user_name', 'email', 'time_creation', 'product')


class UserSerializer(serializers.ModelSerializer):
    # Дополнительне поле для вывода даты последней покупки пользователя
    last_purches = serializers.SerializerMethodField(read_only=True)

    def get_last_purches(self, data):  # data приходит из views.py
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
